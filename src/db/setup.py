from app.db import populate
from app.db.db_manager import DBManager

if __name__ == "__main__":
    # create database and fake data (if doesn't already exist):
    db_exists = DBManager.database_exists()
    if not db_exists:
        DBManager.create_db_if_does_not_exist()
        populate.generate_data()
    else:
        print("Database already exists.")
