#!/usr/bin/env python3
"""Routes module that holds all the routes for the application"""
import json
from flask import redirect, render_template, request
from flask import flash, url_for
from flask_login import login_user, login_required
from flask_login import logout_user, current_user  # type: ignore
from app import app
from app.forms import LoginForm, RegisterForm
from models import storage


@app.route('/')
def home():
    """The home route"""
    return render_template('index.html')

@app.route('/reserve', methods=['GET'])
@login_required
def reserve():
    """The reserve route
    Return all the clinics that are near the user for the specified disease specialty
    """
    # a list of dictionaries containing the diseases
    # their ids, probabilities, and specialties
    diseases = request.cookies.get('diseases', None)

    clinics = []
    if diseases:
        diseases = json.loads(diseases)
        clinics = storage.get("Clinic", filters={"specialty": diseases[0]['specialty']})
    else:
        # get the most rated clinics near the user
        diseases = []
        clinics = storage.get("Clinic")

    # filter the clinics to the clinics that are near the user
    clinics = [clinic for clinic in clinics if abs(clinic.address - current_user.address) <= 0.005]
    return render_template('clinics.html', diseases=diseases, clinics=clinics)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """The login route"""
    form = LoginForm()
    if form.validate_on_submit():
        from models.user import User  # pylint: disable=import-outside-toplevel
        next_page = request.form.get('next_data', 'home')
        try:
            user = storage.get(User, {"email": form.email.data})[0] or None
            if user and user.check_password(form.password.data):
                login_user(user)
                # Update the user current location
                user.latitude = request.form.get('latitude', user.latitude)
                user.longitude = request.form.get('longitude', user.longitude)
                user.save()  # a proper bug here
                return redirect(url_for(next_page.split('/')[-1]))
            flash('Invalid email or password')
            return render_template('login.html', form=form, next_page=next_page)

        except Exception:  # pylint: disable=broad-except
            flash('Invalid email or password', 'danger')
            for field, errors in form.errors.items():
                flash(f"{field}: {errors}", 'danger')
            return render_template('login.html', form=form, next_page=next_page)

    if '/login' in request.url:
        return render_template('login.html', form=form, next_page='home')
    return render_template('login.html', form=form, next_page=request.url.split('/')[-1])

@app.route('/register', methods=['GET', 'POST'])
def register():
    """The register route"""
    form = RegisterForm()
    if form.validate_on_submit():
        from models.user import User  # pylint: disable=import-outside-toplevel
        next_page = request.form.get('next_page', 'home')
        try:
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
                age=form.age.data,
                gender=form.gender.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                phone=form.phone.data,
                profile_image=form.profile_image.data
            )
            user.save()
            login_user(user)
            flash('Account created successfully')
            return redirect(url_for(next_page))
        except Exception as e:  # pylint: disable=broad-except
            # log the error
            print(e)
            storage.rollback()
            flash('An error occurred, please try again')
            return render_template('register.html', form=form, next_page=next_page), 500

    next_page = request.args.get('next_page', url_for('home'))
    return render_template('register.html', form=form, next_page=next_page)


@app.route('/logout')
def logout():
    """The logout route"""
    logout_user()
    return redirect(url_for('home'))
