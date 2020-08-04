# -*- coding: utf-8 -*-
import os
import sys

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djaludir.settings')

# required if using django models
import django
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from djimix.core.database import get_connection
from djimix.core.database import xsql

import argparse


# set up command-line options
desc = """
    Find deceased folks.
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test'
)


def main():
    """Find deceased alumni."""
    sql = '''
        SELECT
            *
        FROM
            profile_rec
        WHERE
            decsd_date IS NOT NULL
        ORDER BY id
    '''

    if test:
        print(sql)

    with get_connection() as connection:
        results = xsql(sql, connection, key='debug')
        rows = results.fetchall()

        for row in rows:
            print(row)


if __name__ == '__main__':
    args = parser.parse_args()
    test = args.test

    if test:
        print(args)

    sys.exit(main())
