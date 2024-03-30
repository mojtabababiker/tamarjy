#!/usr/bin/env python3
"""API v1 app module"""
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.routes import app_routes
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_routes)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def close_session(exception):
    """Close session"""
    try:
        storage.close()
    except Exception:
        #log the error
        pass


@app.errorhandler(404)
def not_found(error):
    """Not found"""
    #log the error
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host="localhost", port=5050)
