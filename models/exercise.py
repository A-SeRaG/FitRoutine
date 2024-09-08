#!/usr/bin/python
""" holds class Exercise"""
import models
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Exercise(BaseModel, Base):
    """Representation of Exercise """
    __tablename__ = 'exercises'
    target_muscle = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    rest_period_in_seconds = Column(Integer, nullable=False, default=0)
    sets = Column(Integer, nullable=False, default=0)
    reviews = relationship("Review",
                            backref="exercises",
                            cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes Exercise"""
        super().__init__(*args, **kwargs)


    @property
    def reviews(self):
        """getter attribute returns the list of Review instances"""
        review_list = []
        all_reviews = models.storage.all(Review)
        for review in all_reviews.values():
            if review.exercise_id == self.id:
                review_list.append(review)
        return review_list
