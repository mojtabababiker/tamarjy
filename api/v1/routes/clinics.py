#!/usr/bin/env python
"""API clinics view module"""
from flask import jsonify, request
from api.v1.routes import app_routes
from models import storage, TIME_FORMAT
from models.appointment import Appointment


@app_routes.route('/clinics', methods=['GET'])
def get_clinics():
    """Get all clinics for the provided disease that are near the user"""
    specialty = request.args.get('specialty')
    user_id = request.args.get('user_id')
    if not specialty:
        return jsonify({"error": "Missing specialty for the current user"}), 400
    if not user_id:
        return jsonify({"error": "Authentication problem please re login and try again"}), 400

    user = storage.get('User', filters={'id': user_id})
    if not user or not user[0]:
        return jsonify({"error": "Authentication problem please re login and try again"}), 404
    user = user[0]
    clinics = storage.get('Clinic', filters={'specialty': specialty})
    print(clinics)
    if not clinics:
        return jsonify({"error": "No clinics found for the provided Disease"}), 400

    clinics_list = []
    # filter the clinics to the clinics that are near the user
    clinics = [clinic for clinic in clinics if abs(clinic.address - user.address) <= 0.055]
    for clinic_ in clinics:
        clinic_dict = {
            'id': clinic_.id,
            'name': clinic_.name,
            'specialty': clinic_.specialty,
            'image': clinic_.profile_image,
            'phone': clinic_.phone,
        }
        clinics_list.append(clinic_dict)

    print(clinics_list)
    return jsonify({"data": clinics_list, "status": "success"}), 200

@app_routes.route('clinics/reserve', methods=['POST'])
def reserve_clinic():
    """Reserve a clinic for the user"""
    from datetime import datetime  # pylint: disable=import-outside-toplevel
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'clinic_id' not in data:
        return jsonify({"error": "Missing clinic_id"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400

    clinic = storage.get('Clinic', filters={'id': data['clinic_id']})
    if not clinic or not clinic[0]:
        return jsonify({"error": "Clinic not found"}), 404

    user = storage.get('User', filters={'id': data['user_id']})
    if not user or not user[0]:
        return jsonify({"error": "User not found"}), 404

    # TODO: check if the user already has an appointment with the clinic  # pylint: disable=fixme
    # TODO: check if the clinic is available at the provided date  # pylint: disable=fixme
    appointment_ = Appointment(
        user_id=user[0].id,
        clinic_id=clinic[0].id,
        date=data.get('date', datetime.now().strftime(TIME_FORMAT))
    )
    appointment_.save()
    return jsonify({"message": "Appointment reserved successfully"}), 201
    