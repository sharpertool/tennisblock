update couples set couplename = 
    (select concat(a.lastname,"s")
    from players a
    where couples.pa_id = a.pid)
    ;
