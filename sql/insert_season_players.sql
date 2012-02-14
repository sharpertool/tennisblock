insert into season_players (pid,season,sid,blockmember)
select pid,"2009 spring",3,blockmember from players
where pid not in (3,4)
;
