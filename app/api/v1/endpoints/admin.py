from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import require_role
from app.core.exceptions import UserNotFoundError
from app.db.models import models
from app.db.models.models import UserRole
from app.db.session import get_db
from app.schemas.user import AdminUserRead

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get(
    "/users",
    response_model=List[AdminUserRead],
    dependencies=[Depends(require_role(UserRole.admin))]
)
def list_users(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.User)

    if is_active is not None:
        query = query.filter(models.User.is_active == is_active)

    return query.all()

@router.patch(
    "/users/{user_id}/toggle-active",
    response_model=AdminUserRead,
    dependencies=[Depends(require_role(UserRole.admin))]
)
def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
      raise UserNotFoundError(user_id)

    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)

    return user

@router.patch(
    "/users/{user_id}/toggle-role",
    response_model=AdminUserRead,
    dependencies=[Depends(require_role(UserRole.admin))]
)
def toggle_user_role(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise UserNotFoundError(user_id)

    if user.role == UserRole.admin:
        user.role = UserRole.user
    else:
        user.role = UserRole.admin

    db.commit()
    db.refresh(user)

    return user
