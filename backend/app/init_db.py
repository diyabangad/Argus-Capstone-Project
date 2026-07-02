from app.core.database import Base, engine
from app.models import procurement  # Keeps the model tables registered


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("ARGUS SQLite tables created successfully.")


if __name__ == "__main__":
    create_tables()