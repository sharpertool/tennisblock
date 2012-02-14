create procedure get_teams(   )
modifies sql data
begin
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
            and (m.pid in (select pid from schedule where matchid = 2058))
            and (f.pid in (select pid from schedule where matchid = 2058))
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
    
        

end;
