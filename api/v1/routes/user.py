#!/usr/bin/env python3
"""API users view module"""
from flask import jsonify, request, abort
from api.v1.routes import app_routes
from models import storage
from models.user import User
from models.appointment import Appointment
