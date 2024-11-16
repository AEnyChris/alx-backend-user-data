#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
# import secrets


app = Flask(__name__)
app.register_blueprint(app_views)
# app.config['SECRET_KEY'] = secrets.token_hex(16)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
if os.getenv('AUTH_TYPE') == 'auth':
    auth = Auth()
elif os.getenv('AUTH_TYPE') == 'basic_auth':
    auth = BasicAuth()
elif os.getenv('AUTH_TYPE') == 'session_auth':
    auth = SessionAuth()
elif os.getenv('AUTH_TYPE') == 'session_exp_auth':
    auth = SessionExpAuth()
elif os.getenv('AUTH_TYPE') == 'session_db_auth':
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ request unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ request forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def handle_before_request():
    """handle authorization before handling request"""
    ex_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
            ]
    if auth:
        if auth.require_auth(request.path, ex_paths):
            if auth.authorization_header(request) is None and \
                    auth.session_cookie(request) is None:
                abort(401)
            cur_user = auth.current_user(request)
            if cur_user is None:
                abort(403)
            else:
                request.current_user = cur_user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
