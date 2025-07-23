from sqlalchemy import Column, Integer, Float, String
from database import Base

class Candlesticks(Base):
    __tablename__ = "candlesticks"

    id = Column(Integer, primary_key=True, index= True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

    