import os
from pymysql import install_as_MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")

install_as_MySQLdb()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=NullPool,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        print("db close")
        session.close()
