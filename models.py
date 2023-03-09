from sqlalchemy import String, Integer, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from enum import Enum
from datetime import datetime

class Status(Enum):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'

Base = declarative_base()



class AppUser(Base):
    __tablename__ = "appuser"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(30))
    password = Column(String(64))
    tasks = relationship("Task", backref="appuser", lazy=True, cascade="all, delete-orphan" )

    def __str__(self):
        return f"UserName: {self.name}"


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    description = Column(String(128))
    status = Column(Enum(Status), default=Status.PENDING, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('appuser.id'), nullable=False)
    
