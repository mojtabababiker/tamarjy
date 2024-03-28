#!/usr/bin/env python3
"""Flask app that run the web application"""
import secrets
from flask import Flask, flash
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# configure the app
app = Flask(__name__)
app.url_map.strict_slashes = False
app.secret_key = secrets.token_urlsafe(16)

csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    """The user loader function"""
    from models import storage
    try:
        return storage.get('User', filters={'id': user_id})[0]
    except Exception:
        return None
@login_manager.unauthorized_handler
def unauthorized():
    """The unauthorized function"""
    from app.routes import login
    flash('Login Required')
    return login()

@app.teardown_appcontext
def close_session(exception):
    """Close the session"""
    try:
        from models import storage
        storage.close()
    except Exception:
        pass

_app = app  # prevent overwriting the app variable with the app module
from app.routes import *
if __name__ == '__main__':
    _app.run(host='localhost', port=5500, debug=True)
