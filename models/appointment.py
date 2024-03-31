#!/usr/bin/env python
"""holds the appointment model class"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from models import TIME_FORMAT
from models.base_model import BaseModel, Base


class Appointment(BaseModel, Base):
    """appointment model class"""
    __tablename__ = 'appointments'
    user_id = Column(String(64), ForeignKey('users.id'), nullable=False)
    clinic_id = Column(String(64), ForeignKey('clinics.id'), nullable=False)
    date = Column(DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        """initiate the appointment model"""
        if 'date' in kwargs:
            self.date = datetime.strptime(kwargs['date'], TIME_FORMAT)
        super().__init__(*args, **kwargs)

    @property
    def time(self):
        """get the time of the appointment in the format HH:MM"""
        return self.date.strftime('%H:%M')

    @property
    def day(self):
        """get the day of the appointment in the format YYYY-MM-DD"""
        return self.date.strftime('%Y-%m-%d')
