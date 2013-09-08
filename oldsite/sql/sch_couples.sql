# Get a list of coules that have NOT played
select distinct coupleid
from couples,schedule,blockmeetings 
where 
    (select count(*) from schedule) = 0 or
    (pa_id not in (select pid from schedule)
    and pb_id not in (select pid from schedule))
    ;

select count(coupleid) nplays,coupleid,meetid,date
from couples,schedule,blockmeetings 
where 
    schedule.matchid = blockmeetings.meetid 
    and (pa_id = pid or pb_id = pid)
group by coupleid
order by nplays asc,date
    	;

