#!/usr/bin/env python
"""holds the disease model class"""
from sqlalchemy import Column, String, Text
from models.base_model import BaseModel, Base


class Disease(BaseModel, Base):
    """disease model class"""
    __tablename__ = 'diseases'
    name = Column(String(64), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    precautions = Column(Text, nullable=False)
    specialty = Column(String(64), nullable=False)

    def __str__(self) -> str:
        return f"Disease: {self.name} Specialty: {self.specialty} \
            Description: {self.description[:20]}... \
            Precautions: {self.precautions[:20]}..."

    def to_dict(self):
        """return a dictionary representation of the object"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'precautions': self.precautions,
            'specialty': self.specialty
        }
