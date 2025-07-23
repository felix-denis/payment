from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://root:hB4pAciulFdcD2neVkHPNIPFv2EpEu2c@dpg-d20glj6mcj7s73b5jgag-a.ohio-postgres.render.com/trading_epa3"

engine = create_engine(db_url)

localSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = localSession()
    try:
        yield
    finally:
        db.close()

