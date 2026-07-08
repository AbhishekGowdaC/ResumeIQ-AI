from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base ,sessionmaker
from dotenv import load_dotenv
import os

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2]/".env")

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
    )
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()