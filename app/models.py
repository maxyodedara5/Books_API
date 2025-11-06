from database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(
        Integer,
        ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE"),
        primary_key=True,
    )
    book_id = Column(
        Integer,
        ForeignKey(f"{Book.__tablename__}.id", ondelete="CASCADE"),
        primary_key=True,
    )
