#!/usr/bin/env python3
"""API v1 views module"""
from flask import Blueprint


app_routes = Blueprint('app_routes', __name__, url_prefix='/api/v1')

from api.v1.routes.user import *
from api.v1.routes.disease import *
from api.v1.routes.clinics import *
