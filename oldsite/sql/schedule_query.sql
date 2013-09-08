SELECT
    firstname,
    lastame,
    gender,
    NTRP,
    microNTRP,
    email,
    home,
    cell,
    work,
    date,
    comments,
    sub
from
    blockmeetings bm, schedule s, players p
where 
    bm.matchid = s.matchid
    and s.pid = p.pid
    and bm.matchid = 1
order by
    gender,p.pid

