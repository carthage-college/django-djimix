    SELECT
    UNIQUE
    CASE
        WHEN
            NVL(UPPER(stu_serv_rec.bldg), '') = 'CMTR'
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
    cc_student_medical_manager.id as manid,
    cc_student_medical_manager.sitrep,
    cc_student_medical_manager.athlete, cc_student_medical_manager.sports,
    cc_student_medical_manager.cc_student_immunization,
    cc_student_medical_manager.cc_student_meni_waiver,
    cc_student_medical_manager.cc_athlete_privacy_waiver,
    cc_student_medical_manager.cc_athlete_reporting_waiver,
    cc_student_medical_manager.cc_athlete_risk_waiver,
    cc_student_medical_manager.cc_athlete_sicklecell_waiver,
    cc_athlete_sicklecell_waiver.id as sicklecell_id,
    cc_athlete_sicklecell_waiver.updated_at,
    cc_athlete_sicklecell_waiver.waive,
    cc_athlete_sicklecell_waiver.proof,
    cc_athlete_sicklecell_waiver.results,
    cc_athlete_privacy_waiver.id as privacy_id,
    cc_athlete_privacy_waiver.news_media,
    cc_athlete_privacy_waiver.parents_guardians,
    cc_athlete_privacy_waiver.disclose_records,
    cc_student_meni_waiver.id as menid,
    cc_athlete_risk_waiver.id as risk_id,
    cc_athlete_reporting_waiver.id as reporting_id,
    profile_rec.birth_date,
    profile_rec.sex,
    mobile_rec.phone as mobile,
    prog_enr_rec.subprog,
    prog_enr_rec.lv_date,
    prog_enr_rec.acst,
    stu_acad_rec.sess,
    prog_enr_rec.cl,
    mobile_rec.phone as mobile
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
    cc_student_medical_manager ON id_rec.id = cc_student_medical_manager.college_id
LEFT JOIN
    cc_student_meni_waiver ON cc_student_medical_manager.id = cc_student_meni_waiver.manager_id
LEFT JOIN
    cc_athlete_sicklecell_waiver ON id_rec.id = cc_athlete_sicklecell_waiver.college_id
    AND
        (cc_athlete_sicklecell_waiver.proof = 1 or cc_athlete_sicklecell_waiver.created_at > DATE("06/01/15"))
LEFT JOIN
    cc_athlete_privacy_waiver ON cc_student_medical_manager.id = cc_athlete_privacy_waiver.manager_id
LEFT JOIN
    cc_athlete_risk_waiver ON cc_student_medical_manager.id = cc_athlete_risk_waiver.manager_id
LEFT JOIN
    cc_athlete_reporting_waiver ON cc_student_medical_manager.id = cc_athlete_reporting_waiver.manager_id
LEFT JOIN
    profile_rec  ON  id_rec.id = profile_rec.id
LEFT JOIN
    stu_serv_rec    ON  id_rec.id   =   stu_serv_rec.id
LEFT JOIN
    aa_rec as mobile_rec on
    (id_rec.id = mobile_rec.id AND mobile_rec.aa = "ENS")
WHERE
    id_rec.id =
AND
    stu_serv_rec.yr = "2017"
AND stu_serv_rec.sess   =
  CASE
    WHEN month(CURRENT) > 7 THEN "RA"
    ELSE "RC"
  END
/*

Cataldo, Omar

AND
    id_rec.lastname =
AND
    id_rec.firstname =
    id_rec.id =
AND
    stu_serv_rec.sess in ("GA","GB","GC","GE","RA","RC","AM","GC","PC","TC")
AND
    stu_serv_rec.sess in ("RA","RC","AM","GC","PC","TC")
*/
