from datetime import datetime
from enum import Enum

from sqlalchemy import Column, String, Integer, DateTime, Boolean

from app.db.database import Base

class UserRole(str, Enum):
  user = "user"
  admin = "admin"

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  username = Column(String, nullable=False, unique=True, index=True)
  email = Column(String, nullable=False, unique=True, index=True)
  hashed_password = Column(String, nullable=False, unique=False, index=False)
  user_role = Column(String, default="user", nullable=False, unique=False, index=True)
  is_active = Column(Boolean, default=True, nullable=False, unique=False, index=True)
  created_at = Column(DateTime, default=datetime.utcnow, index=False)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=False)