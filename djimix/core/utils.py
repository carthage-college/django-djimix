from django.conf import settings
from django.core.validators import validate_email
from djimix.core.database import get_connection, xsql

import re


def get_uuid(email):
    """Obtains the UUID based on the provided email address."""
    row = None
    if validate_email(email):
        sql = "SELECT * FROM fwk_user WHERE email='{}'".format(email)
        connection = get_connection(settings.MSSQL_EARL, encoding=False)
        with connection:
            results = xsql(sql, connection)
            row = results.fetchone()
    return row


def get_userid(jenzabarUserID):
    """Obtains the user ID based on the UUID provided."""
    # prevent folks from submitting anything but the fwk_user id
    #reggie="([\w\-\.]+[\-\.][\w\-\.]+)(\d+)\-(\w+)"
    #reggie="(\{{0,1}([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}\}{0,1})"
    #reggie="([0-9a-fA-F]){8}(-([0-9a-fA-F]){4}){3}-([0-9a-fA-F]){12}"
    #reggie ='^[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{12}$'
    # below works
    reggie='\w{8}-(\w{4}-){3}\w{12}'
    # works
    #reggie ='^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
    # works
    #reggie = '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    pattern = re.compile(reggie)
    if not pattern.match(jenzabarUserID):
        return None
    try:
        # for SQLServer, you must use single quotes in the SQL incantation,
        # otherwise it barfs for some reason
        sql = "SELECT * FROM fwk_user WHERE id='{}'".format(jenzabarUserID)
        connection = get_connection(settings.MSSQL_EARL, encoding=False)
        # automatically closes the connection after leaving 'with' block
        with connection:
            results = xsql(sql, connection, key='debug')
            row = results.fetchone()
        return row[5]
    except:
        return None
