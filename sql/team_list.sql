select
    ta_pa.pid   tapa, concat(ta_pa.firstname," ",ta_pa.lastname) tapanm,
    ta_pb.pid   tapb, concat(ta_pb.firstname," ",ta_pb.lastname) tapbnm,
    ta_pa.NTRP + ta_pb.NTRP taCombineeNTRP,
    tb_pa.pid   tbpa, concat(tb_pa.firstname," ",tb_pa.lastname) tbpanm,
    tb_pb.pid   tbpb, concat(tb_pb.firstname," ",tb_pb.lastname) tbpbnm,
    tb_pa.NTRP + tb_pb.NTRP tbCombineeNTRP,
    abs((ta_pa.NTRP + ta_pb.NTRP)-(tb_pa.NTRP + tb_pb.NTRP)) NTRPDiff,
    concat(LPAD(ta_pa.pid,3,"00"),":",lpad(ta_pb.pid,3,"00"),":",lpad(tb_pa.pid,3,"00"),":",lpad(tb_pb.pid,3,"00")) combokey
from
    players ta_pa,
    players ta_pb,
    players tb_pa,
    players tb_pb
    
where 
        (ta_pa.pid in (select pid from schedule where matchid = 2058))
    and (ta_pb.pid in (select pid from schedule where matchid = 2058))
    and (tb_pa.pid in (select pid from schedule where matchid = 2058))
    and (tb_pb.pid in (select pid from schedule where matchid = 2058))
    and (ta_pa.pid not in (select pid from slots where meetid = 2058 and setnum = 1))
    and (ta_pb.pid not in (select pid from slots where meetid = 2058 and setnum = 1))
    and (tb_pa.pid not in (select pid from slots where meetid = 2058 and setnum = 1))
    and (tb_pb.pid not in (select pid from slots where meetid = 2058 and setnum = 1))
    and ta_pa.gender = "m"
    and ta_pb.gender = "f"
    and tb_pa.gender = "m"
    and tb_pb.gender = "f"
    and ta_pa.pid != tb_pa.pid
    and ta_pb.pid != tb_pb.pid
    and ta_pa.pid < tb_pa.pid
    and concat(LPAD(ta_pa.pid,3,"00"),":",lpad(ta_pb.pid,3,"00"),":",lpad(tb_pa.pid,3,"00"),":",lpad(tb_pb.pid,3,"00")) not in (select combokey from slots)

order by NTRPDiff
;    

select * 
from teams t1,teams t2, teams t3
where 
        t1.ta_pa.pid not in (select pid from teams where teamid = t2.teamid or teamid = t3.teamid)
    and t1.ta_pb.pid not in (t2.ta_pa.pid,t2.tb_pa.pid,t3.ta_pa.pid,t2.tb_pa.pid)
    and t1.tb_pa.pid not in (t2.ta_pa.pid,t2.tb_pa.pid,t3.ta_pa.pid,t2.tb_pa.pid)
    and t1.tb_pb.pid not in (t2.ta_pa.pid,t2.tb_pa.pid,t3.ta_pa.pid,t2.tb_pa.pid)

