from django.conf import settings
from django.core.cache import cache

from djimix.core.database import xsql
from djimix.sql.departments import (
    ACADEMIC_DEPARTMENTS, ALL_DEPARTMENTS,
    DEPARTMENT_FACULTY, DEPARTMENT_DIVISION_CHAIRS,
    FACULTY_DEPTS, PERSON_DEPARTMENTS, STAFF_DEPTS
)


def department(code):
    """
    returns the department given the three letter code
    """

    results = None
    sql = "{} AND hrdept = '{}' ORDER BY DESCR".format(ALL_DEPARTMENTS,code)
    obj = xsql(sql)
    if obj:
         results = obj.fetchone()
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
