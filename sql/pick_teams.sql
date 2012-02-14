drop table if exists tmp_couples;
create table tmp_couples (
        cid         integer(16) NOT NULL auto_increment,
        m_pid       integer(16),
        m_name      varchar(60),
        m_ntrp      float,
        m_untrp     float,
        f_pid       integer(8),
        f_name      varchar(60),
        f_ntrp      float,
        f_untrp     float,
        c_ntrp      float,
        c_untrp     float,
        primary key (`cid`)
    );

insert into tmp_couples (
        m_pid,
        m_name,
        m_ntrp,
        m_untrp,
        f_pid,
        f_name,
        f_ntrp,
        f_untrp,
        c_ntrp,
        c_untrp
    )
select
    m.pid m_id,
    concat(m.firstname," ",m.lastname) m_name,
    m.NTRP m_ntrp,
    m.microNTRP m_untrp,
    f.pid f_id,
    concat(f.firstname," ",f.lastname) f_name,
    f.NTRP f_ntrp,
    f.microNTRP f_untrp,
    m.NTRP + f.NTRP c_ntrp,
    m.microNTRP + f.microNTRP c_untrp
    
from players m,players f
where 
        m.gender = 'f' 
    and f.gender = 'm'
    and (m.pid in (select pid from schedule where matchid = 2078))
    and (f.pid in (select pid from schedule where matchid = 2078))
;
select * from tmp_couples;

