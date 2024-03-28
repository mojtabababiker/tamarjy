#!/usr/bin/env python3
"""holds the base model class for all the models in the application"""

from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from models import storage


Base = declarative_base()


class BaseModel:
    """Base model class for all the models in the application"""
    id = Column(String(64), primary_key=True, nullable=False, default=str(uuid4()))
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, **kwargs) -> None:
        """initiate the class"""
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if 'id' not in kwargs:
                self.id = str(uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)

    def save(self):
        """save the model instance to the database"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self):
        """delete the model instance from the database"""
        storage.delete(self)

    def update(self, **kwargs):
        """update the model instance"""
        for key, value in kwargs.items():
            if key != '__class__':
                setattr(self, key, value)
        self.updated_at = datetime.now()
        storage.save()
