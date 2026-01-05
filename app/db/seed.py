from app.db.session import SessionLocal
from app.db.models.models import User, Task, StatusEnum, UserRole
from app.core.security import get_password_hash

#ejecuto con python -m app.db.seed

def seed_data():
    db = SessionLocal()
    try:
        print("Iniciando seed...")

        user = User(
            username="mili",
            email="mili@test.com",
            hashed_password=get_password_hash("123456"),
            role=UserRole.user
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        admin = User(
            username="admin",
            email="admin@gmail.com",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.admin
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

        task1 = Task(
            title="Comprar alimentos",
            description="Ir al súper",
            status=StatusEnum.pending,
            user_id=user.id
        )

        task2 = Task(
            title="Estudiar Python",
            description="Práctica de SQLAlchemy",
            status=StatusEnum.in_progress,
            user_id=user.id
        )

        db.add_all([task1, task2])
        db.commit()

        print("Seed ejecutado correctamente")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
