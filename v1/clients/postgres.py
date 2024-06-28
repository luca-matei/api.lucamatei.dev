from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from v1.config import settings


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.Base = declarative_base()
            self.engine = create_engine(settings.POSTGRES_DSN)
            self.Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            self._initialized = True

    @contextmanager
    def session_scope(self) -> Generator:
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as exc:
            session.rollback()
            raise
        finally:
            session.close()


# Usage example
db = Database()


@contextmanager
def PostgresSession() -> Generator:
    with db.session_scope() as session:
        yield session
