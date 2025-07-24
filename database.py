from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://root:vFPYpd7l7xzoSdAiTrjB53ethKQw9nMm@dpg-d211a015pdvs739iu950-a.singapore-postgres.render.com/trading_wj9m"

engine = create_engine(db_url)

localSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = localSession()
    try:
        yield
    finally:
        db.close()

