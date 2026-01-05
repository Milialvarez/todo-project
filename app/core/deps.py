from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.jwt import decode_access_token
from app.db.session import get_db
from app.db.models import models
from app.db.models.models import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def require_role(role: UserRole):
    def dependency(current_user: models.User = Depends(get_current_user)):
        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return dependency

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    
    if db.query(models.RevokedToken).filter(
        models.RevokedToken.token == token # check the sent token is still allowed
    ).first():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revoked",
        )

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401)

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401)

    user = db.query(models.User).filter(
        models.User.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(status_code=401)

    return user


def get_current_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    if db.query(models.RevokedToken).filter(
        models.RevokedToken.token == token
    ).first():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revoked"
        )

    decode_access_token(token)
    return token
