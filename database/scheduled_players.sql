delimiter $$

drop procedure if exists scheduled_players$$

create procedure scheduled_players(
    p_meeting_id INT
    )
BEGIN

    create temporary table if not exists 
    meeting_guys as select * from scheduled_players
    where meeting_id = p_meeting_id and gender='M';

    create temporary table if not exists 
    meeting_gals as select * from scheduled_players
    where meeting_id = p_meeting_id and gender='F';

    create temporary table if not exists 
    meeting_guys2 as select * from scheduled_players
    where meeting_id = p_meeting_id and gender='M';

    create temporary table if not exists 
    meeting_gals2 as select * from scheduled_players
    where meeting_id = p_meeting_id and gender='F';

    select
        a.pid guy_pid,
        concat(a.first, ' ', a.last) as guy,
        a.ntrp guy_ntrp,
        a.microntrp guy_untrp,
        a.issub as guysub,
        b.pid gal_pid,
        concat(b.first, ' ', b.last) as gal,
        b.ntrp gal_ntrp,
        b.microntrp gal_untrp,
        b.issub as galsub,
        b.partner_id
    from 
        meeting_guys a
        left outer join
        meeting_gals b
        on a.partner_id = b.pid

    union

    select
        a.pid guy_pid,
        concat(a.first, ' ', a.last) as guy,
        a.ntrp guy_ntrp,
        a.microntrp guy_untrp,
        a.issub as guysub,
        b.pid gal_pid,
        concat(b.first, ' ', b.last) as gal,
        b.ntrp gal_ntrp,
        b.microntrp gal_untrp,
        b.issub as galsub,
        b.partner_id
    from 
        meeting_guys2 a
        right outer join
        meeting_gals2 b
        on b.partner_id = a.pid
    ;
    
    drop temporary table if exists meeting_guys;
    drop temporary table if exists meeting_gals;
    drop temporary table if exists meeting_guys2;
    drop temporary table if exists meeting_gals2;
    
END
$$

delimiter ;



