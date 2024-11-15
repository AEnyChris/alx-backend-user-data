#!/usr/bin/env python3
"""Creates a new Flask view that handles
all routes for the Session authentication.
"""
import os
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from flask import abort


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """handles login authentication"""
    if request:
        email = request.form.get('email')
        password = request.form.get('password')
        if not email:
            return jsonify({"error": "email missing"}), 400
        if not password:
            return jsonify({"error": "password missing"}), 400

        user = User.search({'email': email})

        if not user:
            return jsonify({"error": "no user found for this email"}), 404
        if not user[0].is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth
        session_id = auth.create_session(user[0].id)
        res = jsonify(user[0].to_json())
        res.set_cookie(os.getenv('SESSION_NAME'), session_id)
        # session[os.getenv('SESSION_NAME')] = session_id
        return res


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def delete_session():
    """deletes a sesision/logout"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
