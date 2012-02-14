select count(*) numplays
from blockmeetings bm, schedule s
where
    bm.meetid = s.matchid
    and s.pid = 16
    and bm.date < '2008-10-10'
    
;