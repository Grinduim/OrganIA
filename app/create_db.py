from sqlalchemy_utils import database_exists, create_database
from app.db import engine, Base


def reset_database():
    # Check if the database exists; create it if it doesn't
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database '{engine.url.database}' created.")
    else:
        print(f"Database '{engine.url.database}' already exists.")

    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    print("Dropped all tables.")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Created all tables.")


if __name__ == "__main__":
    reset_database()