drop table if exists tmp_sets;

create table tmp_sets (
        setid   integer(16) NOT NULL auto_increment,
        m1_m1_pid integer(16),
        m1_f1_pid integer(16),
        m1_m2_pid integer(16),
        m1_f2_pid integer(16),

        m2_m1_pid integer(16),
        m2_f1_pid integer(16),
        m2_m2_pid integer(16),
        m2_f2_pid integer(16),

        m3_m1_pid integer(16),
        m3_f1_pid integer(16),
        m3_m2_pid integer(16),
        m3_f2_pid integer(16),

        m4_m1_pid integer(16),
        m4_f1_pid integer(16),
        m4_m2_pid integer(16),
        m4_f2_pid integer(16),

        primary key (`setid`)
    );
    
insert into tmp_sets (
    m1_m1_pid,
    m1_f1_pid,
    m1_m2_pid,
    m1_f2_pid,
    m2_m1_pid,
    m2_f1_pid,
    m2_m2_pid,
    m2_f2_pid,
    m3_m1_pid,
    m3_f1_pid,
    m3_m2_pid,
    m3_f2_pid,
    m4_m1_pid,
    m4_f1_pid,
    m4_m2_pid,
    m4_f2_pid
    )
    
select
    m1.m1_pid,
    m1.f1_pid,
    m1.m2_pid,
    m1.f2_pid,

    m2.m1_pid,
    m2.f1_pid,
    m2.m2_pid,
    m2.f2_pid,

    m3.m1_pid,
    m3.f1_pid,
    m3.m2_pid,
    m3.f2_pid,
    
    m4.m1_pid,
    m4.f1_pid,
    m4.m2_pid,
    m4.f2_pid
from
    tmp_matches m1,tmp_matches m2,tmp_matches m3,tmp_matches m4
    
where
    1
    and m1.m1_pid not in (m2.m1_pid,m2.m2_pid,m3.m1_pid,m3.m2_pid,m4.m1_pid,m4.m2_pid)
    and m1.f1_pid not in (m2.f1_pid,m2.f2_pid,m3.f1_pid,m3.f2_pid,m4.f1_pid,m4.f2_pid)
    and m1.m2_pid not in (m2.m1_pid,m2.m2_pid,m3.m1_pid,m3.m2_pid,m4.m1_pid,m4.m2_pid)
    and m1.f2_pid not in (m2.f1_pid,m2.f2_pid,m3.f1_pid,m3.f2_pid,m4.f1_pid,m4.f2_pid)
                                     
    and m2.m1_pid not in (m1.m1_pid,m1.m2_pid,m3.m1_pid,m3.m2_pid,m4.m1_pid,m4.m2_pid)
    and m2.f1_pid not in (m1.f1_pid,m1.f2_pid,m3.f1_pid,m3.f2_pid,m4.f1_pid,m4.f2_pid)
    and m2.m2_pid not in (m1.m1_pid,m1.m2_pid,m3.m1_pid,m3.m2_pid,m4.m1_pid,m4.m2_pid)
    and m2.f2_pid not in (m1.f1_pid,m1.f2_pid,m3.f1_pid,m3.f2_pid,m4.f1_pid,m4.f2_pid)

    and m3.m1_pid not in (m2.m1_pid,m2.m2_pid,m1.m1_pid,m1.m2_pid,m4.m1_pid,m4.m2_pid)
    and m3.f1_pid not in (m2.f1_pid,m2.f2_pid,m1.f1_pid,m1.f2_pid,m4.f1_pid,m4.f2_pid)
    and m3.m2_pid not in (m2.m1_pid,m2.m2_pid,m1.m1_pid,m1.m2_pid,m4.m1_pid,m4.m2_pid)
    and m3.f2_pid not in (m2.f1_pid,m2.f2_pid,m1.f1_pid,m1.f2_pid,m4.f1_pid,m4.f2_pid)
    
    and m4.m1_pid not in (m2.m1_pid,m2.m2_pid,m1.m1_pid,m1.m2_pid,m3.m1_pid,m3.m2_pid)
    and m4.f1_pid not in (m2.f1_pid,m2.f2_pid,m1.f1_pid,m1.f2_pid,m3.f1_pid,m3.f2_pid)
    and m4.m2_pid not in (m2.m1_pid,m2.m2_pid,m1.m1_pid,m1.m2_pid,m3.m1_pid,m3.m2_pid)
    and m4.f2_pid not in (m2.f1_pid,m2.f2_pid,m1.f1_pid,m1.f2_pid,m3.f1_pid,m3.f2_pid)
;

