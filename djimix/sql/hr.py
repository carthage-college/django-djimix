FACSTAFF_ALPHA = """
SELECT
    unique id_rec.id, profile_rec.priv_code,
    profile_rec.birth_date, job_rec.descr, job_rec.job_title, job_rec.title_rank,
    TRIM(id_rec.firstname) as firstname, TRIM(id_rec.lastname) as lastname,
    TRIM(aname_rec.line1) as alt_name,
    id_rec.addr_line1, id_rec.addr_line2, id_rec.city, id_rec.st, id_rec.zip,
    id_rec.phone, aa_rec.line2 as spouse, aa_rec.line3 as office_location,
    hrdept_table.descr as department,
    aa_rec.phone as office_phone,
    cvid_rec.ldap_name,
    TRIM(trim(email_rec.line1) || trim(email_rec.line2) || trim(email_rec.line3)) AS email
FROM
    id_rec
    LEFT JOIN cvid_rec on id_rec.id = cvid_rec.cx_id
    LEFT JOIN profile_rec on id_rec.id = profile_rec.id
    LEFT JOIN aa_rec on (
        id_rec.id = aa_rec.id
    AND
        aa_rec.aa = "SCHL"
    AND
        (aa_rec.end_date >= TODAY or aa_rec.end_date is null)
    )
    LEFT JOIN aa_rec as aname_rec on (
        id_rec.id = aname_rec.id AND aname_rec.aa = "ANDR"
    )
    LEFT JOIN aa_rec as email_rec on (
        id_rec.id = email_rec.id AND email_rec.aa = "EML1"
    ),
    job_rec, pos_table, hrdept_table
WHERE
    job_rec.id = id_rec.id
AND
    job_rec.tpos_no = pos_table.tpos_no
AND
    job_rec.beg_date <= TODAY
AND
    (job_rec.end_date > ADD_MONTHS(TODAY,-3) or job_rec.end_date is null)
AND
    pos_table.active_date <= TODAY
AND
    hrdept_table.hrdept = pos_table.pcn_03
AND
    hrdept_table.hrdiv not in ("EMER")
AND
    (pos_table.inactive_date is null or pos_table.inactive_date > TODAY)
AND
    email_rec.end_date is null
AND
    job_rec.title_rank is not null
AND
    job_rec.title_rank != ""
AND
    job_rec.hrpay != "DPW"
"""
