#!/usr/bin/env python3
"""Creates a class to add an expiration date session"""
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """session expiration class"""
    def __init__(self):
        """initializtion"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception as e:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create a new session"""
        session_id = super().create_session(user_id)
        if session_id:
            session_dictionary = {}
            session_dictionary['user_id'] = user_id
            session_dictionary['created_at'] = datetime.now()
            self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns user id based on session id"""
        if session_id:
            session_dict = self.user_id_by_session_id.get(session_id)
            if session_dict:
                user = session_dict.get('user_id')
                c_at = session_dict.get('created_at')
                delta = timedelta(seconds=self.session_duration)
                if self.session_duration <= 0:
                    return user
                if not c_at:
                    return None
                if c_at + delta < datetime.now():
                    return None
                return user
