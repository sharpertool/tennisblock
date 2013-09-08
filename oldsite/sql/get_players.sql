select
    coupleid,
    firstname,
    lastname,
    gender,
    NTRP,
    microNTRP,
    email

from players p,couples c
where 
    (p.pid = c.pa_id or p.pid = c.pb_id)
    and p.blockmember = 1
    and c.blockcouple = 1

order by coupleid,gender desc


