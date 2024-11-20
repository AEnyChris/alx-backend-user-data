#!/usr/bin/env python3
"""authentication module"""
import uuid
import bcrypt
from typing import Union
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns bytes
    The returned bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw.
    """
    byte_password = password.encode()
    hashed = bcrypt.hashpw(byte_password, bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """generates and returns a new uuid string representation"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initializer"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a user with the given email and password"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashpwd = _hash_password(password).decode()
            user = self._db.add_user(email=email, hashed_password=hashpwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """validate required user credentials"""
        try:
            user = self._db.find_user_by(email=email)
            byte_pwd = password.encode()
            hashed_pwd = user.hashed_password.encode()
            if bcrypt.checkpw(byte_pwd, hashed_pwd):
                return True
            return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """
        Find the user corresponding to the email,
        generate a new UUID and store it in the
        database as the user’s session_id,
        then return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            pass

    def get_user_by_session_id(self, session_id: str) -> Union[User, None]:
        """returns the user for a given session"""
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None
        return None
