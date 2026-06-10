from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from app.db.database import Base

class Client(Base):
  __tablename__ = "clients"

  id = Column(Integer, primary_key=True, index=True)
  first_name = Column(String(50), nullable=False)
  last_name = Column(String(50))
  email = Column(String(50), unique=True, index=True)
  phone_number = Column(String(20), nullable=False, unique=True, index=True)
  notes = Column(Text)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)