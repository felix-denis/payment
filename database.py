from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "mysql+mysqlconnector://droot:denohgt3@localhost:3306/trading"

engine = create_engine(db_url)

localSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = localSession()
    try:
        yield
    finally:
        db.close()

