from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://root:q6OznSu396ANzGCEQ3283eeCorTQAzb0@dpg-d20etd6uk2gs73c76p60-a.oregon-postgres.render.com/trading_g3r0"

engine = create_engine(db_url)

localSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = localSession()
    try:
        yield
    finally:
        db.close()

