from database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, text


class Book(Base):
    __tablename__ = "sqlaclh"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 

