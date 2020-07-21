# -*- coding: utf-8 -*-

"""Database utilities for pyodbc."""

from django.conf import settings

import pyodbc
import sys


def get_connection(earl=None, encoding=True):
    """Establish an ODBC connection to a database."""
    if not earl:
        earl = settings.INFORMIX_ODBC

    count = 0
    # sometimes we cannot connect to the database, so we attempt
    # a number of times before failing. currently 100 attempts.
    while True:
        try:
            cnxn = pyodbc.connect(earl)
            break
        except pyodbc.Error:
            count += 1
            if count < 100:
                pass
            else:
                cnxn = None
                break

    if cnxn and encoding:
        if sys.version_info >= (3,):
            # Python 3.x
            cnxn.setencoding(encoding='utf-8')
            cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
            cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
            cnxn.setdecoding(
                pyodbc.SQL_WMETADATA,
                encoding='utf-32le',
                ctype=pyodbc.SQL_CHAR,
            )
        else:
            # Python 2.7
            cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='cp1252')
            cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='cp1252')
            cnxn.setencoding(str, encoding='utf-8')
            cnxn.setencoding(unicode, encoding='utf-8')

    return cnxn


def xsql(sql, connection=None, key=None):
    """Executes the SQL queries against Informix using ODBC."""
    if not connection:
        connection = get_connection()

    rows = None
    if connection:
        cursor = connection.cursor()
        if key == 'debug':
            rows = cursor.execute(sql)
        else:
            # while loop is needed because informix barfs from
            # time to time. 10 is the current threshhold.
            count = 0
            while count < 10:
                try:
                    rows = cursor.execute(sql)
                    break
                except pyodbc.Error:
                    count += 1
    return rows
