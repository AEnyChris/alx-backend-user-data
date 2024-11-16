#!/usr/bin/env python3
"""Create a new authentication class for
saving session info in database"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """create as class for saving session info in database"""
    def create_session(self, user_id=None):
        """creates and stores new instance of
        UserSession and returns the Session ID"""
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            return user_session.session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting
        UserSession in the database based on session_id"""
        if session_id:
            UserSession.load_from_file()
            user_session = UserSession.search({'session_id': session_id})
            if user_session:
                if super().user_id_for_session_id(session_id):
                    return user_session[0].user_id

    def destroy_session(self, request=None):
        """destroys the UserSession based on
        the Session ID from the request cookie"""
        session_id = self.session_cookie.get(request)
        obj_list = User.search({'session_id': session_id})
        if obj_list:
            obj_list[0].remove()
            return True
        return False
