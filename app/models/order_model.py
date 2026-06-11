from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base

class OrderStatus(str, Enum):
  measurements = "measurements"
  quoting = "quoting"
  awaiting_deposit = "awaiting_deposit"
  ordering_material = "ordering_material"
  in_production = "in_production"
  instalation = "instalation"
  completed = "completed"
  cancellde = "cancelled"

class Order(Base):
  __tablename__ = "orders"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(100), nullable=False)
  status = Column(String, default="measurements", nullable=False, index=True)
  client = relationship("Client", back_populates="orders")
  client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
  delivery_address = Column(String(200), nullable=False)
  deal_size = Column(Numeric(10, 2), default=0.00)
  esimated_hours = Column(Numeric(6, 2), default=0.00, nullable=False)
  actual_hours = Column(Numeric(6, 2), default=00)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  is_deleted = Column(Boolean, default=False, nullable=False)