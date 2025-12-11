from .session import engine
from .models import Base

#script to test conection and create tables
def init():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created!")

if __name__ == "__main__":
    init()
