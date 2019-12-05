from django.conf import settings

import pyodbc


def get_connection(earl=None, encoding=True):
    """
    establish an ODBC connection to a database
    """
    if not earl:
        earl = settings.INFORMIX_ODBC

    count = 0
    # sometimes we cannot connect to the database, so we attempt
    # a number of times before failing. currently 100 attempts.
    while True:
        try:
            cnxn = pyodbc.connect(earl)
            break
        except:
            count += 1
            if count < 100:
                pass
            else:
                cnxn = None
                break

    if encoding:
        try:
            # Python 3.x
            # production
            cnxn.setencoding(encoding='utf-8')
            cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='cp1252')
            cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='cp1252')
            cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-32le', ctype=pyodbc.SQL_CHAR)
        except:
            # Python 2.7
            cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='cp1252')
            cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='cp1252')
            cnxn.setencoding(str, encoding='utf-8')
            cnxn.setencoding(unicode, encoding='utf-8')

    return cnxn


def xsql(sql, connection=None, key=None):
    """
    helper method that executes the SQL queries against Informix using
    ODBC
    """

    if not connection:
        connection = get_connection()

    cursor = connection.cursor()
    if key == "debug":
        objects = cursor.execute(sql)
    else:
        # while loop is need because informix barfs from
        # time to time. 10 is the current threshhold.
        count = 0
        while True:
            try:
                objects = cursor.execute(sql)
                break
            except:
                count += 1
                if count < 10:
                    pass
                else:
                    objects = None
                    break

    return objects
