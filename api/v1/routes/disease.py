#!/usr/bin/env python3
"""API diseases view module"""
import json
from flask import jsonify, request, abort, make_response
from api.v1.routes import app_routes
from models import storage, predictor


@app_routes.route('/predict', methods=['POST'])
def predict():
    """Predict a disease based on the provided symptoms"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'symptoms' not in data:
        return jsonify({"error": "Missing symptoms"}), 400
    symptoms = data['symptoms']
    if not symptoms:
        return jsonify({"error": "Symptoms must not be empty"}), 400
    prediction = predictor.predict(symptoms)
    if prediction is None:
        return jsonify({"error":
                        "An error occurred while predicting, please try again"}), 500
    if not prediction:
        return jsonify({"error": "No diseases found for the provided symptoms"}), 400
    diseases = []
    for disease, prob in prediction.items():
        try:
            disease_dict = {
                'disease_name': disease,
                'probability': prob
            }
            dis = storage.get('Disease', filters={'name': disease})[0]
            disease_dict['disease_id'] = dis.id
            disease_dict['specialty'] = dis.specialty
        except Exception:  # pylint: disable=broad-except
            # log the query error
            disease_dict['disease_id'] = "NAN"
            disease_dict['specialty'] = "NAN"
        diseases.append(disease_dict)
    res = make_response(jsonify({"diseases": diseases}), 200)
    diseases_json = json.dumps(diseases)
    res.set_cookie('diseases', diseases_json, max_age=600, domain='localhost')
    return res

@app_routes.route('/diseases/<disease_id>', methods=['GET'])
def get_disease_info(disease_id):
    """Get a disease information[description, precaution, and specialty] by its id"""
    disease = storage.get('Disease', filters={'id': disease_id})
    if not disease:
        abort(404)
    disease = disease[0]
    return jsonify(disease.to_dict()), 200
