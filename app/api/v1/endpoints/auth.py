from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.deps import get_current_token
from app.db.session import get_db
from app.db.models import models
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.config import settings
from app.schemas.token import Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=str(user.id), expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(
    token: str = Depends(get_current_token),
    db: Session = Depends(get_db),
):
    exists = db.query(models.RevokedToken).filter(
        models.RevokedToken.token == token
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Token already revoked")

    revoked = models.RevokedToken(token=token)
    db.add(revoked)
    db.commit()

    return {"message": "Logout successful"}