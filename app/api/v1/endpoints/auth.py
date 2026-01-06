from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.deps import get_current_token
from app.db.session import get_db
from app.db.models import models
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token, decode_access_token
from app.core.config import settings
from app.schemas.token import Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    refresh_token = create_refresh_token(
        subject=str(user.id),
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    db_refresh = models.RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=datetime.utcnow()
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    db.add(db_refresh)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post("/logout")
def logout(
    token: str = Depends(get_current_token),
    refresh_token: str | None = None,
    db: Session = Depends(get_db)
):
    db.add(models.RevokedToken(token=token))

    if refresh_token:
        db.query(models.RefreshToken).filter(
            models.RefreshToken.token == refresh_token
        ).update({"revoked": True})

    db.commit()
    return {"message": "Logout successful"}


@router.post("/refresh", response_model=Token)
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    payload = decode_access_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    stored_token = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == refresh_token,
        models.RefreshToken.revoked == False
    ).first()

    if not stored_token:
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    user_id = payload.get("sub")

    new_access_token = create_access_token(
        subject=user_id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token
    }
