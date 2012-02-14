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
    m3_f2_pid
    )
    
select
    c1a.m_pid,
    c1a.f_pid,
    c1b.m_pid,
    c1b.f_pid,

    c2a.m_pid,
    c2a.f_pid,
    c2b.m_pid,
    c2b.f_pid,

    c3a.m_pid,
    c3a.f_pid,
    c3b.m_pid,
    c3b.f_pid
    
from
    tmp_couples c1a, tmp_couples c1b,
    tmp_couples c2a, tmp_couples c2b,
    tmp_couples c3a, tmp_couples c3b
    
where
    1
    and c1a.m_pid not in (c1b.m_pid,c2a.m_pid,c2b.m_pid,c3a.m_pid,c3b.m_pid)
    and c1a.f_pid not in (c1b.f_pid,c2a.f_pid,c2b.f_pid,c3a.f_pid,c3b.f_pid)
    and c1b.m_pid not in (c1a.m_pid,c2a.m_pid,c2b.m_pid,c3a.m_pid,c3b.m_pid)
    and c1b.f_pid not in (c1a.f_pid,c2a.f_pid,c2b.f_pid,c3a.f_pid,c3b.f_pid)
                                     
    and c2a.m_pid not in (c2b.m_pid,c1a.m_pid,c1b.m_pid,c3a.m_pid,c3b.m_pid)
    and c2a.f_pid not in (c2b.f_pid,c1a.f_pid,c1b.f_pid,c3a.f_pid,c3b.f_pid)
    and c2b.m_pid not in (c2a.m_pid,c1a.m_pid,c1b.m_pid,c3a.m_pid,c3b.m_pid)
    and c2b.f_pid not in (c2a.f_pid,c1a.f_pid,c1b.f_pid,c3a.f_pid,c3b.f_pid)

    and c3a.m_pid not in (c3b.m_pid,c2a.m_pid,c2b.m_pid,c1a.m_pid,c1b.m_pid)
    and c3a.f_pid not in (c3b.f_pid,c2a.f_pid,c2b.f_pid,c1a.f_pid,c1b.f_pid)
    and c3b.m_pid not in (c3a.m_pid,c2a.m_pid,c2b.m_pid,c1a.m_pid,c1b.m_pid)
    and c3b.f_pid not in (c3a.f_pid,c2a.f_pid,c2b.f_pid,c1a.f_pid,c1b.f_pid)
;

