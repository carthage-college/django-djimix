# -*- coding: utf-8 -*-

import argparse
import os
import sys

from django.conf import settings
from djimix.core.database import get_connection
from djimix.core.database import xsql


# set up command-line options
desc = """
    Accepts as input an email.
"""

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument(
    '-e',
    '--email',
    required=True,
    help="User ID",
    dest='email',
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def main():
    """Fetch the UUID from the database based on the email provided."""
    sql = "SELECT * FROM fwk_user WHERE email='{}'".format(email)
    connection = get_connection(settings.MSSQL_EARL, encoding=False)
    with connection:
        results = xsql(sql, connection, key='debug')
        row = results.fetchone()
    print(row)


if __name__ == '__main__':
    args = parser.parse_args()
    email = args.email
    test = args.test

    if test:
        print(args)

    sys.exit(main())
