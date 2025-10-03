# app/database.py
from sqlmodel import create_engine, Session

DATABASE_URL = "sqlite:///investors.db"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
