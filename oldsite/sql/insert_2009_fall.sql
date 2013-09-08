insert into `season_players` (pid,season,blockmember)
select pid,'2009 spring',0 from players p
where pid not in (select pid from season_players where season = '2009 spring')
;
