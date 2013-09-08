        select
            a.cid, a.c_untrp,
            b.cid, b.c_untrp,
            truncate(abs(a.c_untrp-b.c_untrp),2) NTRPDiff
            
        from
            tmp_couples a1,tmp_couples b1
            tmp_couples a2,tmp_couples b2
            tmp_couples a3,tmp_couples b3
            tmp_couples a4,tmp_couples b4
        where
            a1.m_pid <> b1.m_pid and a1.f_pid <> b1.f_pid
        order by NTRPDiff
        ;

