SELECT UNIQUE
    id_rec.lastname, id_rec.firstname, id_rec.id, id_rec.ss_no,
    profile_rec.birth_date, stu_serv_rec.bldg,
    id_rec.addr_line1, id_rec.addr_line2, id_rec.city, id_rec.st,
    id_rec.zip, id_rec.ctry, id_rec.phone, cvid_rec.ldap_name,
    adm_rec.plan_enr_sess,
    adm_rec.plan_enr_yr,
    stu_acad_rec.reg_hrs,
    prog_enr_rec.subprog,
    stu_acad_rec.sess,
    prog_enr_rec.acst,
    prog_enr_rec.lv_date,
    prog_enr_rec.cl
FROM
    id_rec
INNER JOIN
    prog_enr_rec ON  id_rec.id = prog_enr_rec.id
LEFT JOIN
    adm_rec     ON  id_rec.id = adm_rec.id
LEFT JOIN
    cvid_rec     ON  id_rec.id = cvid_rec.cx_id
LEFT JOIN
    stu_acad_rec ON  id_rec.id = stu_acad_rec.id
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
LEFT JOIN
    stu_serv_rec  ON  id_rec.id = stu_serv_rec.id
WHERE
    id_rec.id =
AND
    prog_enr_rec.lv_date    IS  NULL
AND
    stu_acad_rec.reg_hrs > 0
/*
    id_rec.lastname = ""
    id_rec.lastname = ""
*/
