drop view if exists tmp_players_view;
create view tmp_players_view as
select 
    p.pid
    firstname,
    lastname,
    gender,
    NTRP,
    microNTRP
from players p,tmp_players tp
where
    p.pid = tp.pid
    ;
