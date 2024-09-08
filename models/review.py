#!/usr/bin/python
""" holds class Review"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer


class Review(BaseModel, Base):
    """Representation of Review """
    __tablename__ = 'reviews'
    exercise_id = Column(String(60), ForeignKey('exercises.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)
    stars = Column(Integer, nullable=False, default=0)

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
