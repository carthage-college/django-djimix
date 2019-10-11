VITALS = '''
SELECT
    UNIQUE
    CASE
        WHEN
            NVL(UPPER(stu_serv_rec.bldg), '') = 'CMTR'
        OR
            NVL(stu_serv_rec.bldg, '') = 'undc'
        OR
            NVL(UPPER(stu_serv_rec.bldg), '') = 'OFF'
        OR
            NVL(UPPER(stu_serv_rec.bldg), '') = ''
        THEN
            'Commuter'
        ELSE
            'Resident'
        END
    AS
        residency_status,stu_serv_rec.stusv_no,
    stu_serv_rec.yr, stu_serv_rec.sess, stu_serv_rec.bldg, stu_serv_rec.room,
    stu_serv_rec.add_date, id_rec.lastname, id_rec.firstname, id_rec.id,
    id_rec.ss_no, id_rec.addr_line1, id_rec.addr_line2, id_rec.city, id_rec.st,
    id_rec.zip, id_rec.ctry, id_rec.phone, cvid_rec.ldap_name,
    adm_rec.plan_enr_sess,adm_rec.plan_enr_yr,
    profile_rec.birth_date, profile_rec.sex, mobile_rec.phone as mobile,
    prog_enr_rec.cl,
    prog_enr_rec.adv_id, prog_enr_rec.subprog, prog_enr_rec.lv_date,
        TRIM(
            CASE
                WHEN TRIM(prog_enr_rec.deg) IN ("BA","BS")
                THEN major1.txt
                ELSE conc1.txt
            END
        ) AS major1,
        TRIM(
            CASE
                WHEN TRIM(prog_enr_rec.deg) IN ("BA","BS")
                THEN major2.txt
                ELSE conc2.txt
            END
        ) AS major2,
        TRIM(
            CASE
                WHEN TRIM(prog_enr_rec.deg) IN ("BA","BS")
                THEN major3.txt
                ELSE ""
            END
        ) AS major3,
    mobile_rec.phone as mobile
FROM
    id_rec
INNER JOIN
    prog_enr_rec ON  id_rec.id = prog_enr_rec.id
LEFT JOIN
    major_table major1  ON  prog_enr_rec.major1    = major1.major
LEFT JOIN
    major_table major2  ON  prog_enr_rec.major2    = major2.major
LEFT JOIN
    major_table major3  ON  prog_enr_rec.major3    = major3.major
LEFT JOIN
    conc_table conc1    ON  prog_enr_rec.conc1     = conc1.conc
LEFT JOIN
    conc_table conc2    ON  prog_enr_rec.conc2     = conc2.conc
LEFT JOIN
    adm_rec     ON  id_rec.id = adm_rec.id
LEFT JOIN
    cvid_rec     ON  id_rec.id = cvid_rec.cx_id
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
LEFT JOIN
    stu_serv_rec    ON  id_rec.id   =   stu_serv_rec.id
LEFT JOIN
    aa_rec as mobile_rec on
    (id_rec.id = mobile_rec.id AND mobile_rec.aa = "ENS")
WHERE
    id_rec.id = {cid}
ORDER BY stu_serv_rec.stusv_no DESC
'''.format
SPORTS = '''
SELECT
    sports
FROM
    cc_student_medical_manager
WHERE
    college_id = {cid}
AND
    created_at > MDY(
        6, 1,
        CASE
          WHEN
            month(CURRENT) < 6
          THEN
            YEAR(TODAY- 1 UNITS YEAR)
          ELSE
            YEAR(TODAY)
        END
    )
'''.format
ADMISSIONS_REP = '''
SELECT
    id_rec.id, id_rec.lastname, id_rec.firstname
FROM
    adm_rec
INNER JOIN
    id_rec ON adm_rec.cnslr_id = id_rec.id
WHERE
    adm_rec.primary_app = 'Y' AND adm_rec.id = {cid}
'''.format
