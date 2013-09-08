        select
            a.cid, a.c_untrp,
            b.cid, b.c_untrp,
            truncate(abs(a.c_untrp-b.c_untrp),2) NTRPDiff
            
        from
            tmp_couples a,tmp_couples b
        where
            a.m_pid <> b.m_pid
            and a.f_pid <> b.f_pid
        order by NTRPDiff
        ;

