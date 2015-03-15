use tennisblock_prod_mirror;

set @mtg=74;

create temporary table if not exists 
meeting_guys as select * from scheduled_players
where meeting_id = @mtg and gender='M';

create temporary table if not exists 
meeting_gals as select * from scheduled_players
where meeting_id = @mtg and gender='F';

create temporary table if not exists 
meeting_guys2 as select * from scheduled_players
where meeting_id = @mtg and gender='M';

create temporary table if not exists 
meeting_gals2 as select * from scheduled_players
where meeting_id = @mtg and gender='F';


select
    a.pid,
    concat(a.first) as guy,
    a.issub as guysub,
    b.pid,
    concat(b.first) as gal,
    b.issub as galsub,
    b.partner_id
from 
    meeting_guys a
    left outer join
    meeting_gals b
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
    meeting_guys2 a
    right outer join
    meeting_gals2 b
    on b.partner_id = a.pid
;
