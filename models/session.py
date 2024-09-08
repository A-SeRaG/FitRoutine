#!/usr/bin/python
""" holds class Session"""
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from datetime import datetime, timedelta

class Session(BaseModel, Base):
    """Representation of an active user session"""
    __tablename__ = 'sessions'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)
    user = relationship("User", back_populates="sessions")

    def __init__(self, *args, **kwargs):
        """Initializes a session"""
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(days=3)
