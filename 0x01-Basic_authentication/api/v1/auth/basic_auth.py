#!/usr/bin/env python3
"""create a basic auth class"""
from api.v1.auth.auth import Auth
import codecs
from models.user import User
from typing import TypeVar
from flask import request


class BasicAuth(Auth):
    """class for basic authentication"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """extracts and returns the base64
        part of the authorization header
        """
        if authorization_header and type(authorization_header) == str:
            if authorization_header.startswith("Basic "):
                return authorization_header.lstrip("Basic ")
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the utf-8 decoded value of
        a Base64 string: base64_authorization_header
        """
        # print(f'base64_auth_header: {base64_authorization_header}')
        if base64_authorization_header:
            if type(base64_authorization_header) == str:
                try:
                    byte_obj = base64_authorization_header.encode()
                    base64_header = codecs.decode(byte_obj, encoding='base64')
                    return base64_header.decode()
                except Exception:
                    return None
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """return the email and password of user
        from a Base64 decoded value otherwise None
        """
        if decoded_base64_authorization_header:
            if type(decoded_base64_authorization_header) == str:
                if ':' in decoded_base64_authorization_header:
                    res = decoded_base64_authorization_header.split(':', 1)
                    return tuple(res)
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if user_email and type(user_email) == str:
            if user_pwd and type(user_pwd) == str:
                User.load_from_file()
                obj = User.search({'email': user_email})
                if obj:
                    if obj[0].is_valid_password(user_pwd):
                        return obj[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request"""
        header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_cred = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_cred[0], user_cred[1])
