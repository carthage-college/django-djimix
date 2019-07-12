from django.conf import settings

import pyodbc


def get_connection(earl=None):
    """
    establish an ODBC connection to a database
    """
    if not earl:
        earl = settings.INFORMIX_ODBC

    cnxn = pyodbc.connect(earl)
    try:
        # Python 3.x
        #cnxn.setencoding(encoding='utf-8', ctype=pyodbc.SQL_CHAR)
        #cnxn.setencoding(encoding='utf8', ctype=pyodbc.SQL_CHAR)
        #cnxn.setencoding(encoding='latin1', ctype=pyodbc.SQL_CHAR)
        #cnxn.setencoding(encoding='cp1252', ctype=pyodbc.SQL_CHAR)

        #cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        #cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='cp1252')
        cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='cp1252')

        #cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='cp1252')
        #cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-16')
        #cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-16le')
        #cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-16be')
        cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-32le')
        #cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8', ctype=pyodbc.SQL_CHAR)

        #utf32b

        #cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='latin1')
        #cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='latin1')
        cnxn.setencoding(encoding='utf-8')
        #cnxn.setencoding(encoding='latin1')
        #cnxn.setencoding(encoding='cp1252')
    except:
        # Python 2.7
        #cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        #cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        #cnxn.setencoding(str, encoding='utf-8')
        #cnxn.setencoding(unicode, encoding='utf-8')
        #cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='latin1')
        #cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='latin1')
        #cnxn.setencoding(str, encoding='latin1')
        #cnxn.setencoding(unicode, encoding='latin1')
        cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='cp1252')
        cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='cp1252')
        cnxn.setencoding(str, encoding='utf-8')
        cnxn.setencoding(unicode, encoding='utf-8')

    return cnxn
