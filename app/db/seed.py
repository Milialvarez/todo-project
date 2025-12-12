from app.db.session import SessionLocal
from app.db.models import User, Task, StatusEnum
from app.core.security import get_password_hash 

#ejecuto con python -m app.db.seed

def seed_data():
    db = SessionLocal()

    try:
        # Crear un user
        user = User(
            username="mili",
            email="mili@test.com",
            hashed_password=get_password_hash("123456")
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Crear tasks de prueba
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

        print("Datos insertados con éxito")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
