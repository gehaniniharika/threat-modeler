from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    framework = Column(String(50))  # STRIDE, PASTA, or HYBRID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), index=True)
    role = Column(String(20))  # user or assistant
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ThreatModel(Base):
    __tablename__ = "threat_models"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), index=True)
    name = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    framework = Column(String(50))
    report_content = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Threat(Base):
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("threat_models.id"), index=True)
    title = Column(String(255))
    description = Column(Text)
    severity = Column(String(50))
    category = Column(String(100))
    mitigation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DataFlow(Base):
    __tablename__ = "data_flows"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("threat_models.id"), index=True)
    source = Column(String(255))
    destination = Column(String(255))
    data_type = Column(String(255))
    protocol = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
