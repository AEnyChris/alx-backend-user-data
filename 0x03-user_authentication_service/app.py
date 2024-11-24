#!/usr/bin/env python3
"""A simple flask app"""
from flask import Flask, jsonify, request, abort
from flask import redirect, url_for
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def index():
    """index route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """endpoint to register a new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email:
        try:
            AUTH.register_user(email, password)
            return jsonify({"email": email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """login user endpoint"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = jsonify({"email": f"{email}", "message": "logged in"})
        res.set_cookie('session_id', session_id)
        return res
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout user endpoint"""
    session_id = request.cookies.get('session_id')
    # print(f'session_id: {session_id}')
    if session_id:
        print('I got a session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect(url_for('index', method='GET'))
    # print(f'Oops I no session_id or user. Session id = {session_id}')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def proflie():
    """endpoint to get user profile"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": f"{user.email}"}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """endpoint to get reset password token"""
    email = request.form.get('email')
    if email:
        try:
            reset_token = AUTH.get_reset_password_token(email)
        except ValueError:
            abort(403)
        return jsonify({"email": f"{email}", "reset_token": f"{reset_token}"})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """endpoint to update password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": f"{email}", "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
