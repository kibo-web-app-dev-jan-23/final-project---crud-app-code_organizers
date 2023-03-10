from enum import Enum
from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Status(Enum):
    PENDING = 'Pending'
    IN_PROGRESS = 'In progress'
    DONE = 'Done'


class AppUser(Base):
    __tablename__ = "appuser"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(30), unique=True)
    password = Column(String(64))
    tasks = relationship("Task", backref="appuser", lazy=True, cascade="all, delete-orphan" )



class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    description = Column(String(128))
    status = Column(Status, default=Status.PENDING, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('appuser.id'), nullable=False)
    
