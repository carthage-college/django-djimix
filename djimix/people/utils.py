from django.conf import settings
from django.core.cache import cache

from djimix.core.database import xsql
from djimix.sql.hr import CID_FROM_EMAIL, POSITION


def get_cid(email):
    """
    obtain a college ID from an email address
    """
    cid = None
    obj = xsql(CID_FROM_EMAIL(email=email)).fetchone()
    if obj:
        cid = obj.id
    return cid


def get_position(tpos):
    """
    obtains some user information based on job title position number and
    caches the results

    NOTE: this is not very reliable when the position is vacant and/or
    there is an interim appointment
    """

    key = 'TPOS_{}'.format(tpos)
    results = cache.get(key)
    if not results:
        sql = POSITION(tpos=tpos)
        results = xsql(sql).fetchone()
        if not results:
            results = settings.TPOS_DEFAULT[tpos]
        cache.set(key, results, None)
    return results
