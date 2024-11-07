#!/usr/bin/env python3
"""A script to obfuscate certain fields in log message"""
import re
from typing import List
import logging


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initializes an instance"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats log records to hide sensitive data"""
        recmsg = super(RedactingFormatter, self).format(record)
        res = filter_datum(self.fields, self.REDACTION, recmsg, self.SEPARATOR)
        return res
