#!/usr/bin/env python3
"""Creates a class to manage the API authentication."""
from flask import request
from typing import List, TypeVar

class Auth:
    """class to manage the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentication"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith('/'):
            path = path + '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """get authorization header"""
        if request is None or request.headers.get('Authorization') is None:
            print(f'request.headers.get: {request.headers.get("Authorization")}')
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """get currect user"""
        return None
