#!/usr/bin/env python3
"""Creates a class to manage the API authentication."""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """class to manage the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentication"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        check = True
        if not path.endswith('/'):
            path = path + '/'
        for p in excluded_paths:
            if p.endswith('*'):
                p = p.rstrip('*') + '.*'
            if re.match(p, path):
                print(f'p: {p} path: {path}')
                check = False
        return check
        """
        if not path.endswith('/'):
            path = path + '/'
        if path not in excluded_paths:
            return True
        return False"""

    def authorization_header(self, request=None) -> str:
        """get authorization header"""
        if request is None:
            return None
        header = request.headers.get('Authorization')
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """get current user"""
        return None
