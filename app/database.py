import os
from os.path import dirname, join

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


DATABASE_PASSWORD = os.environ.get("PASSWORD")
USER = os.environ.get("USER")

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{DATABASE_PASSWORD}@localhost/books_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()