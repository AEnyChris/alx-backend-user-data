#!/usr/bin/env python3
"""authentication module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns bytes
    The returned bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw.
    """
    byte_password = password.encode()
    hashed = bcrypt.hashpw(byte_password, bcrypt.gensalt())
    return hashed
