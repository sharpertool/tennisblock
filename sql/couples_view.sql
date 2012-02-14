drop view if exists couples_view;
create view couples_view as
select 
    coupleid,
    couplename,
    concat(pa.firstname," ",pa.lastname) hisname,
    pa.blockmember paonblock,
    concat(pb.firstname," ",pb.lastname) hername,
    pb.blockmember pbonblock,
    fulltime
from couples c, players pa, players pb
where
    (c.pa_id = pa.pid or c.pa_id = pb.pid) 
    and (c.pb_id = pb.pid or c.pb_id = pa.pid)
    and pa.gender = 'm' and pb.gender = 'f'
    ;
