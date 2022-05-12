#!/usr/bin/env python3
"""A module for filtering logs.
"""
import re
import logging
from typing import List, Tuple
from datetime import datetime


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}


def asc_time() -> str:
    """Returns the current time.
    """
    cur_time = datetime.now()
    cur_time_ms = cur_time.microsecond // 1000
    return str('{},{}'.format(cur_time.strftime("%F %X"), cur_time_ms))


def get_values(record: logging.LogRecord, msg: str) -> Tuple[str]:
    """Retrieves values to be printed for a log record.
    """
    asctime = asc_time()
    return (record.name, record.levelname, asctime, msg.replace(';', '; '))


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """Filters a log line.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a LogRecord.
        """
        tmp = record.getMessage()
        msg = filter_datum(self.fields, self.REDACTION, tmp, self.SEPARATOR)
        values = get_values(record, msg)
        return self.FORMAT % dict(zip(self.FORMAT_FIELDS, values))