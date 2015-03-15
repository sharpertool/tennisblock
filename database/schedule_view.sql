use tennisblock_prod_mirror;

drop view if exists scheduled_players;

create view scheduled_players as
select 
    a.id as pid, 
    a.first, a.last, a.gender, a.ntrp, a.microntrp, a.email, a.phone, a.user_id,
    b.meeting_id, b.issub, b.verified, b.partner_id
from
    blockdb_player a join
    blockdb_schedule b
    on b.player_id = a.id

    ;
