use friday_tennis;

select 
	count(*) cnt
from
	blockmeetings bm, schedule s
where
	bm.meetid = s.matchid and bm.date = '2009-10-09'

;



