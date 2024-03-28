#!/usr/bin/env python3
"""Form module that holds all the forms for the application"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import IntegerField, StringField, PasswordField, FloatField
from wtforms import SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import storage


class LoginForm(FlaskForm):
    """The login form class"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=12, max=64)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    """The register form class"""
    first_name = StringField('First Name', validators=[DataRequired(),
                                                       Length(max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(),
                                                     Length(max=64)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=12, max=64)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField("Gender", choices=[('Male', 'Male'), ('Female', 'Female')],
                         validators=[DataRequired()])
    profile_image = FileField('Profile Image',
                              validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    longitude = FloatField('Address', validators=[DataRequired()], default=122.00)
    latitude = FloatField('Address', validators=[DataRequired()], default=122.00)
    phone = StringField('Phone Number', validators=[Length(max=64)])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        """The email validation method, check if the email already exists"""
        try:
            user = storage.get('User', {"email": email.data})[0]
            if user:
                raise ValidationError('Email already exists')
        except IndexError:
            pass
