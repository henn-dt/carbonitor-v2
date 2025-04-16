# app/infrastructure/persistence/contexts/dbcontext.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator, Any

class DBContext:
    def __init__(self, connection_string: str):
        self.engine = create_engine(
            connection_string,
            echo=False  # Set to False in production
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        )

    @contextmanager
    def session(self) -> Generator[Session, Any, None]:
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()