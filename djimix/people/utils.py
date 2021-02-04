# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.cache import cache
from djimix.core.database import xsql
from djimix.sql.hr import CID_FROM_EMAIL, POSITION


def get_cid(email):
    """Obtain a college ID from an email address."""
    cid = None
    obj = xsql(CID_FROM_EMAIL(email=email)).fetchone()
    if obj:
        cid = obj.id
    return cid


def get_position(tpos):
    """
    Obtains some user information based on job title position number.

    NOTE: this is not very reliable when the position is vacant and/or
    there is an interim appointment.
    """

    key = 'TPOS_{0}'.format(tpos)
    results = cache.get(key)
    if not results:
        sql = POSITION(tpos=tpos)
        results = xsql(sql).fetchone()
        if not results:
            results = settings.TPOS_DEFAULT.get(tpos)
        cache.set(key, results, None)
    return results


def get_peeps(who):
    """Obtain the folks based on who parameter."""
    key = 'provisioning_vw_{0}_api'.format(who)
    peeps = cache.get(key)

    if peeps is None:

        if who == 'facstaff':
            where = 'faculty IS NOT NULL OR staff IS NOT NULL'
        elif who in ['faculty','staff','student']:
            where = '{0} IS NOT NULL'.format(who)
        else:
            where = None

    if not peeps and where:
        sql = """
            SELECT
                id, lastname, firstname, username
            FROM
                provisioning_vw
            WHERE
                {0}
            ORDER BY
                lastname, firstname
        """.format(where)

        objects = xsql(sql, key=settings.INFORMIX_DEBUG)

        if objects:
            peeps = []
            for obj in objects:
                row = {
                    'cid': obj[0],
                    'lastname': obj[1],
                    'firstname': obj[2],
                    'email': '{0}@carthage.edu'.format(obj[3]),
                    'username': obj[3],
                }
                peeps.append(row)
            cache.set(key, peeps, timeout=86400)

    return peeps
