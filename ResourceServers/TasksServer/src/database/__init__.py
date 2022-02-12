from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USER = 'my_admin'
PASS = 'Jm08sf68SA13nBsd12'
HOST = '185.218.125.97'
PORT = 5432
DB_NAME = 'my_tasks'


SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
