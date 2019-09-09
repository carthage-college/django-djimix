CREATE VIEW cars:provisioning_vw (id, firstname, lastname, username, prox_no, cx_uid, faculty, staff, student, program, birth_date, zip)
AS
select unique id_rec.id as id, 
       trim(id_rec.firstname) as firstname,
       trim(id_rec.lastname) as lastname,
       trim(cvid_rec.ldap_name) as username,
       cvid_rec.prox_no as prox_no,
       userid_table.uid as cx_uid,
       case when fac_job.id is not null then fac_job.hrstat 
            when fac_sec.id is not null then "sec_rec"
            when fac_instr.id is not null then "instr_rec"
            else null 
       end as faculty,
       case when staff.id is not null then staff.hrpay else null end as staff,
       -- the ordering of these when statements is significant. earlier rules are more important. i.e., showing up as a current student in stu_acad_rec means more than merely having a current record in reg_clr
       case when stu_acad.id is not null then "stu"
            when program_enrollment.id is not null then "prog"
            when reg_clear.id is not null then "reg_clear"
            when msw.id is not null then "msw"
            when incoming.id is not null then "incoming"
            else null 
       end as student,       
       case when stu_acad.id is not null then stu_acad.prog || " " || stu_acad.subprog
            when program_enrollment.id is not null then program_enrollment.prog || " " || program_enrollment.subprog
            when incoming.id is not null then incoming.plan_enr_yr || " " || incoming.plan_enr_sess
            else null 
       end as program,
       profile_rec.birth_date,
       id_rec.zip[1,5] as zip
from id_rec
    -- faculty are identified in three overlapping ways: job records,section records and instructor records. Find all possibilities here and wash it out up above via a case statement. 
    left join (
        select unique id, hrstat
        from job_rec 
        where job_rec.hrpay in ("FVW","VKH")
        and job_rec.hrstat in ("FT","PT","TLE","PTGP")
        -- people stay provisioned until the ~end~ of their last day, and to make this work I also had to bump out the imputed end date of open-ended positions
        and nvl(job_rec.end_date,today) >= today 
        ) fac_job 
        on fac_job.id = id_rec.id
    left join (
        select unique sec_rec.fac_id as id
        from  sec_rec, fac_rec, cvid_rec
        where sec_rec.fac_id = cvid_rec.cx_id
          and sec_rec.fac_id = fac_rec.id
          and cvid_rec.ldap_name <> ''
          and (sec_rec.beg_date - 180) <= today
          and (sec_rec.end_date + 90) >= today
        ) fac_sec 
        on fac_sec.id = id_rec.id
    -- also check instr_rec to identify faculty members
    left join (
        select unique instr_rec.id
        from  instr_rec, acad_cal_rec, cvid_rec, fac_rec
        where instr_rec.id = cvid_rec.cx_id
          and instr_rec.id = fac_rec.id
          and cvid_rec.ldap_name <> ''
          and instr_rec.yr = acad_cal_rec.yr
          and instr_rec.sess = acad_cal_rec.sess
          and acad_cal_rec.subsess = ''
          and (acad_cal_rec.beg_date - 180) <= today
          and (acad_cal_rec.end_date + 90) >= today 
        ) fac_instr
        on fac_instr.id = id_rec.id
    -- staff are simply people with certain types of job records        
    left join (
        select unique id, hrpay 
        from job_rec
        where nvl(job_rec.end_date,today) >= today
        and job_rec.hrpay in ("FVW","VEN","K97","VKH")
        and job_rec.hrstat in ("AD","HR","PATH","ADPT","VEND","HRPT")        
        ) staff
        on staff.id = id_rec.id
    left join (
        select unique id, prog, subprog 
        from prog_enr_rec
        where prog_enr_rec.acst IN ('GOOD' ,'LOC' ,'PROB' ,'PROC' ,'PROR' ,'READ' ,'RP' ,'SAB' ,'SHAC' ,'SHOC')
        and subprog not in ("ENRM","PARA") 
        and prog_enr_rec.lv_date IS NULL 
        ) program_enrollment
        on id_rec.id = program_enrollment.id
    left join (  -- this selects all students whose latest stu_acad_rec record is current or in the future, based on session end dates
        select sar.id, sar.prog, sar.subprog, sar.yr, sar.sess
        from stu_acad_rec sar
        join acad_cal_rec acr
            on sar.sess = acr.sess
            and sar.yr = acr.yr
            and today <= NVL(acr.end_date, today)
            and acr.subsess = ' '
        join (select sar.id, max(acr.end_date) as latest_end_date
              from stu_acad_rec sar
              join acad_cal_rec acr
                on sar.yr = acr.yr 
                and sar.sess = acr.sess 
                and trim(acr.subsess) = "" 
                group by sar.id) latest_sess
            on latest_sess.latest_end_date = acr.end_date
            and sar.yr = acr.yr 
            and sar.sess = acr.sess 
            and trim(acr.subsess) = ""
            and sar.id = latest_sess.id   
        where sar.reg_stat IN ('R','C')
        ) stu_acad on id_rec.id = stu_acad.id 
    left join (
        select unique regclr_rec.id
        from regclr_rec
            join acad_cal_rec
                on regclr_rec.sess = acad_cal_rec.sess
                and regclr_rec.yr = acad_cal_rec.yr
                and acad_cal_rec.beg_date <= TODAY + (60)
                and today <= NVL(acad_cal_rec.end_date, today)
                and acad_cal_rec.subsess = ' '
        ) reg_clear on id_rec.id = reg_clear.id 
    left join (
        select unique adm_rec.id
        from adm_rec
        where adm_rec.primary_app = 'Y'
        and adm_rec.subprog = 'MSW'
        and adm_rec.plan_enr_yr >= YEAR(TODAY) - 2
        --and adm_rec.enrstat = 'GRAD' 
    ) msw on id_rec.id = msw.id
    left join (
        select unique ctc_rec.id, adm_rec.plan_enr_yr, adm_rec.plan_enr_sess
        from ctc_rec
            join adm_rec
                on adm_rec.id = ctc_rec.id
                and adm_rec.primary_app = 'Y'
                and ctc_rec.resrc in ('ADVREGDT','INADVREG','TADVREG')
                and ctc_rec.stat in ('C','E')
                and ctc_rec.due_date - 10 <= TODAY
                and ctc_rec.add_date >= TODAY - 390
            join acad_cal_rec
                on adm_rec.plan_enr_sess = acad_cal_rec.sess
                and adm_rec.plan_enr_yr = acad_cal_rec.yr
                and acad_cal_rec.subsess = ' '
                and acad_cal_rec.beg_date <= TODAY + 250
                and TODAY <=  NVL(acad_cal_rec.end_date, TODAY)    
    ) incoming on id_rec.id = incoming.id
    left join cvid_rec 
        on id_rec.id = cvid_rec.cx_id  
    left join profile_rec
        on id_rec.id = profile_rec.id
    left join userid_table
        on id_rec.id = userid_table.id_no
        and nvl(inactive_date,today) >= today
where id_rec.id in (
    -- faculty ids (either in sec_rec, instr_rec or job_rec)
    select unique instr_rec.id
    from  instr_rec, acad_cal_rec, cvid_rec, fac_rec
    where instr_rec.id = cvid_rec.cx_id
      and instr_rec.id = fac_rec.id
      and cvid_rec.ldap_name <> ''
      and instr_rec.yr = acad_cal_rec.yr
      and instr_rec.sess = acad_cal_rec.sess
      and acad_cal_rec.subsess = ''
      and (acad_cal_rec.beg_date - 180) <= today
      and (acad_cal_rec.end_date + 90) >= today 
    
    union
    
    select unique sec_rec.fac_id as id
    from  sec_rec, fac_rec, cvid_rec
    where sec_rec.fac_id = cvid_rec.cx_id
      and sec_rec.fac_id = fac_rec.id
      and cvid_rec.ldap_name <> ''
      and (sec_rec.beg_date - 180) <= today
      and (sec_rec.end_date + 90) >= today
       
    union  
       
    select unique faculty.id 
    from job_rec faculty
        join id_rec on faculty.id = id_rec.id
        join cvid_rec on faculty.id = cvid_rec.cx_id
    where nvl(faculty.end_date,TODAY) >= today 
    and hrpay in ("FVW","VKH")
    and hrstat in ("FT","PT","TLE","PTGP")
    
    union
    
    -- staff ids 
    select unique staff.id
    from job_rec staff
        join id_rec on staff.id = id_rec.id
    where nvl(staff.end_date,today) >= today 
    and hrpay in ("FVW","VEN","K97","VKH")
    and hrstat in ("AD","HR","PATH","ADPT","VEND","HRPT")
    
    union
    
    -- students with an active program enrollment status
    select unique prog_enr_rec.id
    from id_rec 
        join prog_enr_rec
            on id_rec.id = prog_enr_rec.id
            AND prog_enr_rec.lv_date IS NULL 
            AND prog_enr_rec.acst IN ('GOOD' ,'LOC' ,'PROB' ,'PROC' ,'PROR' ,'READ' ,'RP' ,'SAB' ,'SHAC' ,'SHOC')            
            AND prog_enr_rec.subprog != "ENRM"
    union
    
    -- students enrolled in a current or future session
    select sar.id
        from stu_acad_rec sar
        join acad_cal_rec acr
            on sar.sess = acr.sess
            and sar.yr = acr.yr
            and today <= NVL(acr.end_date, today)
            and acr.subsess = ' '
        join (select sar.id, max(acr.end_date) as latest_end_date
              from stu_acad_rec sar
              join acad_cal_rec acr
                on sar.yr = acr.yr 
                and sar.sess = acr.sess 
                and trim(acr.subsess) = "" 
                group by sar.id) latest_sess
            on latest_sess.latest_end_date = acr.end_date
            and sar.yr = acr.yr 
            and sar.sess = acr.sess 
            and trim(acr.subsess) = ""
            and sar.id = latest_sess.id   
        where sar.reg_stat IN ('R','C')

    union
    
    -- students with active regclr_rec records
    select unique regclr_rec.id
    from id_rec
        join regclr_rec 
            on id_rec.id = regclr_rec.id
        join acad_cal_rec
            on regclr_rec.sess = acad_cal_rec.sess
            and regclr_rec.yr = acad_cal_rec.yr
            and acad_cal_rec.beg_date <= TODAY + (60)
            and today <= NVL(acad_cal_rec.end_date, today)
            and acad_cal_rec.subsess = ' '
    
    union
    
    -- MSW students (we use adm_rec since they do not end up appearing in our student information system, but they need to be provisioned for printing, etc.)
    select unique adm_rec.id
    from id_rec 
        join adm_rec
            on id_rec.id = adm_rec.id
            and adm_rec.primary_app = 'Y'
            and adm_rec.subprog = 'MSW'
            and adm_rec.plan_enr_yr >= YEAR(TODAY) - 2
            --and adm_rec.enrstat = 'APPLIED' 
    
    union
    
    -- incoming students
    select unique ctc_rec.id
    from id_rec
        join ctc_rec 
            on id_rec.id = ctc_rec.id
            and ctc_rec.resrc in ('ADVREGDT','INADVREG','TADVREG')
            and ctc_rec.stat in ('C','E')
            and ctc_rec.due_date - 10 <= TODAY
            and ctc_rec.add_date >= TODAY - 390
        join adm_rec
            on adm_rec.id = id_rec.id
            and adm_rec.primary_app = 'Y'
        join acad_cal_rec
            on adm_rec.plan_enr_sess = acad_cal_rec.sess
            and adm_rec.plan_enr_yr = acad_cal_rec.yr
            and acad_cal_rec.subsess = ' '
            and acad_cal_rec.beg_date <= TODAY + 250
            and TODAY <=  NVL(acad_cal_rec.end_date, TODAY)
    
    group by id
)
order by id_rec.id

