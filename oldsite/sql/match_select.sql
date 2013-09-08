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

#select * from tmp_couples;

drop table if exists tmp_pairings;
create table tmp_pairings (a_cid integer(16), b_cid integer(16));

# Now, select a set of distinct couples. This is now the same
# as my first, long query.. but, maybe I can extend this to select
# a set, 4 teams
insert into tmp_pairings (
        a_cid,
        b_cid
    )
select
    a.cid,
    b.cid
from 
    tmp_couples a,tmp_couples b
where
        a.cid != b.cid
    and a.m_pid != b.m_pid
    and a.f_pid != b.f_pid
    and a.m_pid < b.m_pid
 
        ; 

#select * from tmp_pairings;

drop table if exists tmp_matches;

create table tmp_matches (
        matchid   integer(16) NOT NULL auto_increment,
        m1_pid integer(16),
        f1_pid integer(16),
        m2_pid integer(16),
        f2_pid integer(16),
        untrpdiff float(16),
        primary key (`matchid`)
    );

insert into tmp_matches (
    m1_pid,f1_pid,m2_pid,f2_pid,untrpdiff
    )
    
select
    c1a.m_pid,
    c1a.f_pid,
    c1b.m_pid,
    c1b.f_pid,
    truncate(abs(c1a.c_untrp-c1b.c_untrp),2) untrpdiff
    
from
    tmp_couples c1a,
    tmp_couples c1b
    
where
        c1a.m_pid != c1b.m_pid
    and c1a.f_pid != c1b.f_pid
    and c1a.m_pid < c1b.m_pid
    
;

#select * from tmp_matches;


