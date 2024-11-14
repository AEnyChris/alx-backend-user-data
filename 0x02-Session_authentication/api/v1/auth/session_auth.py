#!/usr/bin/env python3
"""Creates a session class"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User
from flask import Flask


class SessionAuth(Auth):
    """Session class to manage session authorization"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id and type(user_id) == str:
            sessionID = str(uuid.uuid4())
            self.user_id_by_session_id[sessionID] = user_id
            return sessionID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id and type(session_id) == str:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request:
            session_id = self.session_cookie(request)
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                del self.user_id_by_session_id[session_id]
                return True
        return False
