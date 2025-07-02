# app/database.py
from sqlmodel import create_engine, SQLModel, Session
from app.config import get_db_url

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(get_db_url(), connect_args={"check_same_thread": False})
    return _engine

def get_session():
    return Session(get_engine())

def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())
