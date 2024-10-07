from sqlalchemy import Column, Integer, String, Date
from app.db import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(Date)
    review = Column(String)
    sentiment = Column(String)
