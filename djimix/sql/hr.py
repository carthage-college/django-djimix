POSITION = '''
    SELECT
        id_rec.id,
        email_rec.line1 as email,
        job_rec.tpos_no
    FROM
        id_rec
    LEFT JOIN job_rec on id_rec.id = job_rec.id
    LEFT JOIN aa_rec as email_rec on
        (id_rec.id = email_rec.id AND email_rec.aa = "EML1")
    WHERE
        job_rec.tpos_no = {tpos}
    AND
        job_rec.end_date IS NULL
'''.format

CID_FROM_EMAIL = '''
    SELECT UNIQUE
        id_rec.lastname, id_rec.firstname, id_rec.id
    FROM
        id_rec
    LEFT JOIN aa_rec as email_rec on
        (id_rec.id = email_rec.id AND email_rec.aa = "EML1")
    WHERE
        email_rec.line1 = "{email}"
'''.format
