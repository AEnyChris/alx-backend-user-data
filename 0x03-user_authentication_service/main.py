#!/usr/bin/env python3
"""Main file"""
import requests
from auth import Auth

PREFIX = 'http://localhost:5000'
AUTH = Auth()


def index() -> None:
    """querying the index route/home page"""
    resp = requests.get(PREFIX + '/')
    # print(resp.headers)
    assert resp.json() == {"message": "Bienvenue"}
    assert resp.status_code == 200


def register_user(email: str, password: str) -> None:
    """querying the register user endpoint"""
    # print('testing register user')
    data = {'email': email, 'password': password}
    resp = requests.post(PREFIX + '/users', data=data)
    try:
        assert resp.status_code == 200
        assert resp.json() == {"email": email, "message": "user created"}
    except AssertionError:
        assert resp.status_code == 400
        assert resp.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """querying loging with wrong password"""
    # print('testing log_in_wrong_password')
    data = {'email': email, 'password': password}
    resp = requests.post(PREFIX + '/sessions', data=data)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """querying loging with wrong password"""
    # print('testing log in')
    data = {'email': email, 'password': password}
    resp = requests.post(PREFIX + '/sessions', data=data)
    assert resp.status_code == 200
    assert resp.json() == {"email": f"{email}", "message": "logged in"}
    assert resp.cookies.get('session_id') is not None
    return resp.cookies.get('session_id')


def profile_unlogged() -> None:
    """checking if profile is unlogged"""
    # print('testing profile_unlogged')
    resp = requests.get(PREFIX + '/profile')
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """querying to see get profile"""
    # print('testing profile_logged')
    resp = requests.get(PREFIX + '/profile',
                        cookies={'session_id': session_id})
    assert resp.status_code == 200
    assert resp.json() == {"email": f"{EMAIL}"}


def log_out(session_id: str) -> None:
    """querying user log out"""
    # print('testing log_out')
    resp = requests.delete(PREFIX + '/sessions',
                           cookies={'session_id': session_id})
    assert resp.json() == {'message': 'Bienvenue'}
    # assert resp.is_redirect


def reset_password_token(email: str) -> str:
    """get reset password token"""
    # print('testing reset_password_token')
    resp = requests.post(PREFIX + '/reset_password', data={'email': email})
    assert resp.status_code == 200
    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """querying update password endpoint"""
    # print('testing update password')
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    resp = requests.put(PREFIX + '/reset_password', data=data)
    assert resp.status_code == 200
    assert resp.json() == {"email": f"{email}", "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    index()

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
    # print(f'reset_token {reset_token}')
    # print(f'session_id {session_id}')
    # print('OK')
