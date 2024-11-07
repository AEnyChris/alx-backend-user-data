#!/usr/bin/env python3
"""A script to obfuscate certain fields in log message"""
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """function to obfuscate message with given redaction"""
    ps = {'p': lambda x, y: r'(?P<f>{})=[^{}]*'.format('|'.join(x), y),
          'repl': lambda x: r'\g<f>={}'.format(x)}
    res = re.sub(ps['p'](fields, separator), ps['repl'](redaction), message)
    return res
