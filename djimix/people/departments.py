from django.conf import settings
from django.core.cache import cache

from djimix.core.database import get_connection, xsql
from djimix.sql.departments import (
    ACADEMIC_DEPARTMENTS, ALL_DEPARTMENTS,
    DEPARTMENT_FACULTY, DEPARTMENT_DIVISION_CHAIRS,
    FACULTY_DEPTS, PERSON_DEPARTMENTS, STAFF_DEPTS,
)
from collections import OrderedDict


def department(code):
    """Returns the department given the three letter code."""
    sql = "{0} AND hrdept = '{1}' ORDER BY DESCR".format(ALL_DEPARTMENTS, code)
    rows = xsql(sql)
    try:
        return rows.fetchone()
    except AttributeError:
        return None


def departments_all_choices():
    """Returns department tuples for choices parameter in models and forms."""
    faculty = xsql(FACULTY_DEPTS)
    staff = xsql(STAFF_DEPTS)
    depts = [('', '---Staff Departments---')]

    if staff:
        for st in staff:
            depts.append((st.hrdept.strip(), st.department.strip()))

    depts.append(('', '---Faculty Deparments---'))

    if faculty:
        for fac in faculty:
            depts.append((fac.pcn_03.strip(), fac.department.strip()))

    return depts


def academic_department(did):
    """Returns academic departments based on department ID."""
    sql = "{0} AND dept_table.dept = '{1}'".format(ACADEMIC_DEPARTMENTS, did)
    rows = xsql(sql)
    try:
        return rows.fetchone()
    except AttributeError:
        return None


def person_departments(cid):
    """Returns all departments to which a person belongs."""
    rows = xsql(PERSON_DEPARTMENTS(college_id=cid))
    try:
        return rows.fetchall()
    except AttributeError:
        return None


def chair_departments(cid):
    """Returns all departments with which a chair/dean is associated."""
    depts = OrderedDict()
    base = """
        SELECT
            dept_table.dept as dept_code, dept_table.txt as dept_name,
            dept_table.div as div_code, div_table.txt as div_name
        FROM
            dept_table
        INNER JOIN
            div_table ON dept_table.div = div_table.div
        WHERE
            CURRENT BETWEEN
                dept_table.active_date
            AND
                NVL(dept_table.inactive_date, CURRENT)
        AND
            dept_table.web_display =   "Y"
    """
    sql = """
        {0}
        AND
            div_table.head_id={1}
        ORDER BY
            dept_table.txt
    """.format(base, cid)

    rows = xsql(sql).fetchall()

    if rows:
        # division dean
        dc = 'dean'
    else:
        # department chair
        dc = 'chair'
        sql = """
            {0}
            AND
                dept_table.head_id={1}
            AND
                dept_table.dept != ("_ESN")
            ORDER BY
            dept_table.txt
        """.format(base, cid)
        rows = xsql(sql).fetchall()
    if rows:
        for row in rows:
            depts[(row.dept_code)] = {
                'dept_name': row.dept_name,
                'dept_code': row.dept_code,
                'div_name':  row.div_name,
                'div_code': row.div_code,
            }
        return ({'depts': depts}, dc, row.div_name, row.div_code)
    else:
        return ({'depts': depts}, None, None, None)


def department_division_chairs(where):
    """Return the department chair and division dean profiles."""
    rows = xsql(DEPARTMENT_DIVISION_CHAIRS(where=where))
    try:
        return rows.fetchall()
    except AttributeError:
        return None


def department_faculty(code, year):
    """Return the faculty for the department given the dept code & year."""
    rows = xsql(DEPARTMENT_FACULTY(year=year, dept=code))
    try:
        return rows.fetchall()
    except AttributeError:
        return None
