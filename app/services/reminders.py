from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.db.models import Reminder
from app.db.models import User

def get_tomorrow_reminders(db: Session):
    tomorrow = date.today() + timedelta(days=1)

    return (
        db.query(Reminder)
        .join(User)
        .filter(Reminder.date == tomorrow)
        .all()
    )
