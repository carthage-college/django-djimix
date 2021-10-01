# returns all departments to which a person belongs
# given the college ID provided by the view
PERSON_DEPARTMENTS = """
SELECT
    unique
    hrdept_table.hrdept as code,
    hrdept_table.descr as department
FROM
    id_rec
LEFT JOIN
    job_rec on (id_rec.id = job_rec.id),
    hrdept_table
WHERE
    id_rec.id = {college_id}
AND
    hrdept_table.end_date is null
AND
    hrdept_table.hrdiv != "EMER"
AND
    hrdept_table.hrdept = job_rec.hrdept
AND
    (job_rec.end_date > TODAY or job_rec.end_date is null)
ORDER BY
    department
""".format
# returns all active academic departments
# NOTE: not as accurrate as FACULTY_DEPTS, i think.
ACADEMIC_DEPARTMENTS = """
    SELECT
        TRIM(dept_table.dept) AS dept_code,
        dept_table.txt as dept_name,
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
        dept_table.web_display = "Y"
    AND
        dept_table.dept not in ("ADV","CART","REGI")
"""

FACULTY_DEPTS = """
SELECT
    unique hrdept_table.descr as department, pos_table.pcn_03
FROM
    pos_table, hrdept_table
WHERE
    pos_table.pcn_01 in ("EXT","FAC","FAD","TLE")
AND
    pos_table.pcn_03 not in (
        "_ATH","ARHU","BUS","_DIS","EDUC","_ENS","_ENT","_ESN","FIAR","_GBL",
        "GM","_GNR","HUMN","IDST","LIS","_MTR","_NAT","NATS","NSSS","PARA",
        "_PEH","PEP","SOCS"
    )
AND
    hrdept_table.hrdiv not in ("EMER","PRDV","VEND")
AND
    hrdept_table.descr not in (
        "Bookstore", "China Internship", "College Official", "EXSS Department",
        "Finance and Accounting", "Officer of the College", "Pending Employee",
        "Professional Studies Div", "Provost's Office", "Student Worker"
    )
AND
    pos_table.pcn_03 = hrdept_table.hrdept
ORDER BY
    department
"""

STAFF_DEPTS = """
SELECT
    unique hrdept_table.descr as department, job_rec.hrdept
FROM
    job_rec, hrdept_table
WHERE
    job_rec.hrdept = hrdept_table.hrdept
AND
    job_rec.hrdept in (
        "ACPR","ADMS","ADUL","ADVS","ARHU","ATH","BOOK","BSOF","CARE",
        "CHAP","COMM","CONF","DOS","EDU","EVS","FINA","FOOD","HCC","HUMR",
        "IA","INEF","INRS","LIS","MAIL","MAIN","NURS","NSSS","PRES","PROV",
        "PRFS","PRST","REGI","RESL","SECU","STAC","STIV","TSI","WRC","WSGC"

    )
AND
    hrdept_table.hrdiv not in ("EMER")
AND
    hrdept_table.descr not in (
        "Food Service Vendor","Officer of the College",
        "Student Success Office","Pending Employee",
        "Student Worker","Bookstore","Athletic Training",
        "Gospel Messengers","Career Services"
    )
ORDER BY
    department
"""

ALL_DEPARTMENTS = """
SELECT
    unique descr, hrdept, hrdiv
FROM
    hrdept_table
WHERE
    end_date IS NULL
AND
    hrdiv IN (
        "ACPR","ADMS","ADUL","ADVS","ARHU","ATH","BOOK","BSOF","CARE",
        "CHAP","CONF","COMM","DOS","EDU","EVS","FINA","FOOD","GM","HCC","HUMR",
        "IA","INEF","INRS","LIS","MAIL","MAIN","NATS","NSSS","PRES","PROV",
        "PRST","REGI","RESL","SECU","STIV","WRC","WSGC",
        "ATDR", "BUSA", "EDUC",
        "NURS", "PRFS", "PRVD",
        "VPAB", "VPAD", "VPCO", "VPCP", "VPEN", "VPIA", "VPLI"
    )
AND
    descr NOT IN (
        "China Internship","Gospel Messengers",
        "Officer of the College","Pending Employee","Student Worker",
        "Student Success Office"
    )
"""
DEPARTMENT_DIVISION_CHAIRS = """
SELECT
    dept_table.dept, dept_table.txt as department_name,
    dept_id.firstname, dept_id.lastname, dept_id.id as deptid,
    dept_email_rec.line1 as dept_email,
    div_table.txt as division_name, div_id.firstname as div_first,
    div_id.lastname as div_last, div_id.id as divid,
    div_email_rec.line1 as div_email
FROM
    dept_table
JOIN
    id_rec
AS
    dept_id
ON
    dept_table.head_id = dept_id.id
JOIN
    div_table
ON
    div_table.div = dept_table.div
JOIN
    id_rec
AS
    div_id
ON
    div_table.head_id = div_id.id
INNER JOIN
    aa_rec
AS
    div_email_rec
ON
    (div_table.head_id = div_email_rec.id AND div_email_rec.aa = "EML1")
INNER JOIN
    aa_rec
AS
    dept_email_rec
ON
    (dept_table.head_id = dept_email_rec.id AND dept_email_rec.aa = "EML1")
WHERE
    NVL(dept_table.inactive_date,today) >= TODAY
AND
    {where}
ORDER BY
    div_table.txt, dept_table.txt


""".format
DEPARTMENT_FACULTY = """
SELECT
    id_rec.id,
    TRIM(id_rec.lastname) AS lastname,
    TRIM(id_rec.firstname) AS firstname,
    TRIM(dept_table.txt) AS txt
FROM
    dept_table
INNER JOIN
    crs_rec
ON
    dept_table.dept = crs_rec.dept
INNER JOIN
    sec_rec
ON
    crs_rec.crs_no = sec_rec.crs_no
AND
    crs_rec.cat = sec_rec.cat
INNER JOIN
    id_rec
ON
    sec_rec.fac_id = id_rec.id
WHERE
    sec_rec.yr >= {year}
AND
    crs_rec.dept == "{dept}"
GROUP BY
    id_rec.id, id_rec.lastname, id_rec.firstname, dept_table.txt
ORDER BY
    txt, lastname, firstname
""".format
