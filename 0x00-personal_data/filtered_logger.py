#!/usr/bin/env python3
"""A script to obfuscate certain fields in log message"""
import re


def filter_datum(fields, redaction, message, separator):
    """function to obfuscate message with given redaction"""
    res = message
    for field in fields:
        res = re.sub(f'{field}=[^{separator}]+{separator}', f'{field}={redaction}{separator}', res)
    return res
