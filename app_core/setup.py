from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import setting

setting = setting.AuthSettings()


class DatabaseSetup:
    def __init__(self):
        self.engine = create_engine(setting.DATABASE_URL)
        self.session_maker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.base = declarative_base()

    def get_session(self) -> sessionmaker:
        return self.session_maker

    def get_base(self):
        return self.base

    def get_engine(self):
        return self.engine


database = DatabaseSetup()
Base = database.get_base()
