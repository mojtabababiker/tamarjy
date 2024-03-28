#!/usr/bin/env python3
"""hold the user model class"""
import os.path
from werkzeug.utils import secure_filename
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.appointment import Appointment  # pylint: disable=unused-import
from app import bcrypt, app


class User(BaseModel, Base):
    """users model class"""
    __tablename__ = 'users'
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    email = Column(String(64), nullable=False)
    password_hash = Column(String(64), nullable=False)
    phone = Column(String(64), nullable=True)
    # address = Column(String(128), nullable=False)
    latitude_ = Column(Float, nullable=True)
    longitude_ = Column(Float, nullable=True)
    gender = Column(String(16), nullable=True)
    age_ = Column(Integer, nullable=False)
    profile_img = Column(String(72), nullable=True)
    appointments = relationship('Appointment', backref='user',
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
    def	longitude(self):
        """return self longitude float point"""
        return self.longitude_

    @longitude.setter
    def	longitude(self, val):
        """set self longitude value"""
        self.longitude_ = float(val)

    @property
    def age(self):
        """return the user age"""
        return self.age_

    @age.setter
    def age(self, age):
        """set the user age"""
        self.age_ = int(age)

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

    @property
    def is_active(self):
        """return True if the user had activated email, False otherwise"""
        return True

    @property
    def is_authenticated(self):
        """return True if the user is authenticated, False otherwise"""
        return self.is_active

    @property
    def is_anonymous(self):
        """return True if the user is anonymous, False otherwise"""
        return False

    def get_id(self):
        """return the user id as a string for login manager purposes"""
        return str(self.id)

    @property
    def password(self):
        """return the user hashed password"""
        return self.password_hash

    @password.setter
    def password(self, password):
        """set the hashed password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """check the provided password validity"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __str__(self):
        """return the user string representation"""
        return f"User: {self.first_name} {self.last_name} \
            Email: <{self.email}> P: <{self.phone or 'NaN'}>"  # type: ignore
