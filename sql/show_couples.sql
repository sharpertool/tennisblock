use friday_tennis;

select 
    coupleid,  
    couplename,
    concat("Name:",a.firstname," ",a.lastname),
    concat("Name:",b.firstname," ",b.lastname)
from couples c,players a,players b
    where c.pa_id = a.pid and c.pb_id = b.pid
;

 select lastname
    from couples c,players a
    where c.pa_id = a.pid
    ;


