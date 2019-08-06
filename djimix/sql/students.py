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
        residency_status, stu_serv_rec.yr, stu_serv_rec.sess, stu_serv_rec.bldg,
    id_rec.lastname, id_rec.firstname, id_rec.id, id_rec.ss_no,
    id_rec.addr_line1, id_rec.addr_line2, id_rec.city, id_rec.st,
    id_rec.zip, id_rec.ctry, id_rec.phone, cvid_rec.ldap_name,
    adm_rec.plan_enr_sess,adm_rec.plan_enr_yr,
    profile_rec.birth_date,
    profile_rec.sex,
    mobile_rec.phone as mobile,
    prog_enr_rec.adv_id,
    prog_enr_rec.subprog,
    prog_enr_rec.lv_date,
    prog_enr_rec.acst,
    stu_acad_rec.sess,
    prog_enr_rec.cl,
    mobile_rec.phone as mobile,
    cc_student_medical_manager.sports
FROM
    id_rec
INNER JOIN
    prog_enr_rec ON  id_rec.id = prog_enr_rec.id
LEFT JOIN
    stu_acad_rec    ON  id_rec.id   =   stu_acad_rec.id
LEFT JOIN
    adm_rec     ON  id_rec.id = adm_rec.id
LEFT JOIN
    cvid_rec     ON  id_rec.id = cvid_rec.cx_id
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
LEFT JOIN
    stu_serv_rec    ON  id_rec.id   =   stu_serv_rec.id
LEFT JOIN
    cc_student_medical_manager ON id_rec.id = cc_student_medical_manager.college_id
LEFT JOIN
    aa_rec as mobile_rec on
    (id_rec.id = mobile_rec.id AND mobile_rec.aa = "ENS")
WHERE
    id_rec.id = {cid}
AND
    cc_student_medical_manager.created_at > MDY(
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
AND
    stu_serv_rec.yr = year(CURRENT)
AND
  stu_serv_rec.sess =
  CASE
    WHEN month(CURRENT) > 6 THEN "RA"
    ELSE "RC"
  END
and
  stu_acad_rec.SESS =
  CASE
    WHEN month(CURRENT) > 6 THEN "RA"
    ELSE "RC"
  END
'''.format
