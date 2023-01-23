from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.common.config import SQLALCHEMY_DATABASE_URL

import pymysql

pymysql.install_as_MySQLdb()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=60
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
