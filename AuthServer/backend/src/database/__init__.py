from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USER = 'my_admin'
PASS = 'DkvtS2A63JhF7aJ92f'
HOST = 'localhost'
PORT = 5432
DB_NAME = 'my_auth'


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
