from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from database import Base

class ThreatModel(Base):
    __tablename__ = "threat_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    framework = Column(String(50))  # STRIDE, PASTA, or ANY
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Threat(Base):
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, index=True)
    title = Column(String(255))
    description = Column(Text)
    severity = Column(String(50))  # Critical, High, Medium, Low
    category = Column(String(100))  # STRIDE category or PASTA phase
    mitigation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DataFlow(Base):
    __tablename__ = "data_flows"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, index=True)
    source = Column(String(255))
    destination = Column(String(255))
    data_type = Column(String(255))
    protocol = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
