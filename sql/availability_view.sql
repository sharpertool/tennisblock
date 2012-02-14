drop view player_availability;
create view player_availability as
select 
	players.pid, 
	firstname, 
	lastname, 
	date,
	unavailable
from players,availability
where players.pid = availability.pid
and availability.unavailable = false
;
drop view player_unavailable ;
create view player_unavailable as
select players.pid, firstname, lastname, date
from players,availability
where players.pid = availability.pid
and availability.unavailable = true
;

select * from player_availability
;




