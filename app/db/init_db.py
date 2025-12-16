from app.db.session import engine
from app.db.models.models import Base

#script to test conection and create tables
def init():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created!")

if __name__ == "__main__":
    init()
