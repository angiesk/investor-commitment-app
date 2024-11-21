from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Enum as SQLAlchemyEnum,
    DateTime,
)
from sqlalchemy.orm import relationship

from app.commons import UserType, InvestorType
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    user_type = Column(SQLAlchemyEnum(UserType), nullable=False)  # Changed here
    email = Column(String, unique=True, index=True)

    # One-to-one relationship with Investor (each user can have one investor)
    investors = relationship("Investor", back_populates="owner", uselist=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Investor(Base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    country = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    investor_type = Column(SQLAlchemyEnum(InvestorType), nullable=False)

    commitments = relationship("Commitment", back_populates="investor")
    owner = relationship("User", back_populates="investors")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Commitment(Base):
    __tablename__ = "commitments"

    id = Column(Integer, primary_key=True, index=True)
    asset_class = Column(String)
    amount = Column(Float)
    currency = Column(String)
    investor_id = Column(Integer, ForeignKey("investors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    investor = relationship("Investor", back_populates="commitments")
