select
	firstname,
	lastname,
	p.pid,
	sp.blockmember

from players p, season_players sp
where 
	p.pid = sp.pid
	and sp.season='2009 spring'

;
	
