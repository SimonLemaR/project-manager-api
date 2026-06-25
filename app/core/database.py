from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


_engine = None


def get_engine():
    global _engine

    if _engine is None:
        _engine = create_engine(settings.DATABASE_URL)

    return _engine


SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
