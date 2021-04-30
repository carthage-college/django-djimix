SELECT UNIQUE
    id_rec.lastname, id_rec.firstname, id_rec.id,
    id_rec.zip, id_rec.ctry, id_rec.phone,
    id_rec.addr_line1, id_rec.addr_line2, id_rec.city,
    id_rec.st, id_rec.zip, id_rec.ctry, id_rec.phone,
    job_rec.job_title,job_rec.title_rank,job_rec.end_date,
    profile_rec.birth_date,profile_rec.sex,
    email_rec.line3 as email,
    cvid_rec.ldap_name, cvid_rec.ldap_add_date
FROM
    id_rec
LEFT JOIN
    profile_rec ON id_rec.id = profile_rec.id
LEFT JOIN
    cvid_rec ON id_rec.id = cvid_rec.cx_id
LEFT JOIN aa_rec as email_rec on
    (id_rec.id = email_rec.id AND email_rec.aa = 'EML1')
LEFT JOIN
    job_rec on id_rec.id = job_rec.id
WHERE
    id_rec.id = {CID}
/*
AND
    id_rec.firstname = ''
AND
    cvid_rec.ldap_name = ''
AND
 */
