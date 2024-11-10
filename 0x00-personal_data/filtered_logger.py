#!/usr/bin/env python3
"""A script to obfuscate certain fields in log message"""
import re
from typing import List
import logging

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


def get_logger() -> logging.Logger:
    """creates a new logger with a StreamHandler and INFO level"""
    logger = logging.getLogger('user data')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.propagate = False
    logger.setLevel('INFO')
    logger.addHandler(stream_handler)
    return logger


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
