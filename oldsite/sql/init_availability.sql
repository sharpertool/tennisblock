delete from availability;

insert into availability
 (PID,date,unavailable,Reason)
select PID, date, 0, ""
from players, blockmeetings
where blockmeetings.holdout = false

