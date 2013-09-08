select *
from couples
where
fulltime = 1
and pa_id not in (select pid from availability where date = '$d' and unavailable=1)
and pb_id not in (select pid from availability where date = '$d' and unavailable=1)
and blockcouple = 1
and season = "2009 spring"
;
