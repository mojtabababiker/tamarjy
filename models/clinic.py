#!/usr/bin/env python
"""holds the clinic model class"""
import os
import os.path
from werkzeug.utils import secure_filename
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from app import app
from models.base_model import BaseModel, Base
from models.appointment import Appointment  # pylint: disable=unused-import


class Clinic(BaseModel, Base):
    """clinic model class"""
    __tablename__ = 'clinics'
    name = Column(String(64), nullable=False)
    #address = Column(String(128), nullable=False)
    latitude_ = Column(Float, nullable=False)
    longitude_ = Column(Float, nullable=False)
    phone = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    doctor = Column(String(64), nullable=False)
    specialty = Column(String(64), nullable=False)
    website = Column(String(128), nullable=True)
    profile_img = Column(String(128), nullable=False, default='default.jpg')
    reservations = relationship('Appointment', backref='clinic',
                            cascade='all, delete-orphan')


    @property
    def address(self):
        """return the summation of the latitude and longitude"""
        try:
            return self.latitude + self.longitude
        except Exception:  # pylint: disable=broad-except
            return None

    @property
    def latitude(self):
        """return self latitude float point"""
        return self.latitude_

    @latitude.setter
    def latitude(self, val):
        """set self latitude value"""
        self.latitude_ = float(val)

    @property
    def longitude(self):
        """return self longitude float point"""
        return self.longitude_

    @longitude.setter
    def longitude(self, val):
        """set self longitude value"""
        self.longitude_ = float(val)

    @property
    def profile_image(self):
        """return the user profile image"""
        return self.profile_img

    @profile_image.setter
    def profile_image(self, profile_image):
        """load the user profile image to the server and
        set the profile_img attribute to the image path
        """
        if profile_image:
            filename_secured = secure_filename(profile_image.filename)
            if filename_secured:
                dir_name = os.path.dirname(app.instance_path)
                extension = filename_secured.split('.')[-1]
                filename = f"{self.id}.{extension}"
                path = os.path.join(dir_name, 'app', 'static', 'images',
                                    'users_images', filename)
                try:
                    # remove the old image if it's exists
                    os.remove(path)
                except Exception:  # pylint: disable=broad-except
                    pass
                profile_image.save(path)
                image_path = f'{self.id}.{extension}'

            else:
                image_path = 'default.jpg'
        else:
            image_path = 'default.jpg'

        self.profile_img = image_path
