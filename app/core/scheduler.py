from apscheduler.schedulers.background import BackgroundScheduler
from app.db.session import SessionLocal
from app.core.email import send_email
from app.services.reminders import get_tomorrow_reminders

scheduler = BackgroundScheduler()

def reminder_job():
    print("⏰ Scheduler ejecutándose...")
    db = SessionLocal()
    try:
        reminders = get_tomorrow_reminders(db)
        print(f"📌 Reminders encontrados: {len(reminders)}")

        for reminder in reminders:
            print(f"📨 Enviando mail a {reminder.user.email}")
            send_email(
                to=reminder.user.email,
                subject="⏰ Recordatorio",
                body=f"Mañana tenés este recordatorio:\n\n{reminder.description}"
            )
    except Exception as e:
        print("❌ Error en scheduler:", e)
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        reminder_job,
        trigger="cron",
        hour=9  
    )
    scheduler.start()