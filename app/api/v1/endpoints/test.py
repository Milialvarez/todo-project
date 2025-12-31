from fastapi import APIRouter, Depends, HTTPException
from pytest import Session

from app.core.email import send_email
from app.db.models.models import Reminder, Task, User
from app.db.session import get_db


router = APIRouter(prefix="/test", tags=["test"])

@router.get("/test-email")
def test_email():
    send_email(
        to="mialvarez@alumnos.exa.unicen.edu.ar",
        subject="Test",
        body="Si llega esto, SMTP funciona"
    )
    return {"ok": True}

@router.delete("/users/by-email/{email}")
def delete_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # borrar tasks
    db.query(Task).filter(Task.user_id == user.id).delete(synchronize_session=False)

    # borrar reminders
    db.query(Reminder).filter(Reminder.user_id == user.id).delete(synchronize_session=False)

    db.delete(user)
    db.commit()

    return {"message": f"User {email} deleted"}

