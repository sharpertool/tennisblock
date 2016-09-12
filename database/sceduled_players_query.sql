create temporary table if not exists 
meeting as select * from scheduled_players
where meeting_id = 74;

select
    a.pid,
    concat(a.first) as guy,
    a.issub as guysub,
    b.pid,
    concat(b.first) as gal,
    b.issub as galsub,
    b.partner_id
from 
    (select * from meeting where gender = 'M') a
    left outer join
    (select * from meeting where gender = 'F') b
    on a.partner_id = b.pid

union

select
    a.pid,
    concat(a.first) as guy,
    a.issub as guysub,
    b.pid,
    concat(b.first) as gal,
    b.issub as galsub,
    b.partner_id
from 
    (select * from meeting where gender = 'M') a
    right outer join
    (select * from meeting where gender = 'F') b
    on a.partner_id = b.pid
;



