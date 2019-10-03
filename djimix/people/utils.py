from django.conf import settings
from django.core.cache import cache

from djimix.core.utils import xsql
from djimix.sql.hr import (
    ACADEMIC_DEPARTMENTS, ALL_DEPARTMENTS, CID_FROM_EMAIL,
    DEPARTMENT_FACULTY, DEPARTMENT_DIVISION_CHAIRS,
    FACULTY_DEPTS, PERSON_DEPARTMENTS, POSITION, STAFF_DEPTS
)


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
        results = xsql(sql)
        if results:
            results = results.fetchone()
        else:
            results = settings.TPOS_DEFAULT[tpos]
        cache.set(key, results, None)
    return results


def department(code):
    """
    returns the department given the three letter code
    """

    results = None
    sql = "{} AND hrdept = '{}' ORDER BY DESCR".format(ALL_DEPARTMENTS,code)
    obj = xsql(sql)
    if obj:
         results = obj.first()
    return results


def departments_all_choices():
    """
    Generate a tuple of department tuples for choices parameter in
    models and forms
    """

    faculty = xsql(FACULTY_DEPTS)
    staff = xsql(STAFF_DEPTS)
    depts = [('','---Staff Departments---')]

    if staff:
        for s in staff:
            depts.append((s.hrdept, s.department))

    depts.append(('', '---Faculty Deparments---'))

    if faculty:
        for f in faculty:
            depts.append((f.pcn_03, f.department))

    return depts
