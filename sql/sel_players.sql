select
p.pid,
coupleid,
firstname,
lastname,
gender,
NTRP,
microNTRP,
email,
home,
work,
cell

from players p,season_players sp,couples c
where
sp.season = '2009 spring'
and c.season = '2009 spring'
and p.pid = sp.pid
and (p.pid = c.pa_id or p.pid = c.pb_id)
and sp.blockmember = 1
and c.blockcouple = 1

order by coupleid, gender desc
;

