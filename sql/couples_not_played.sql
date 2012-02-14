            select distinct coupleid
            from couples,schedule,availability,blockmeetings 
            where
            couples.season = '2009 spring'
            and fulltime = 0
            and pa_id not in (select pid from schedule where season = '2009 spring')
            and pb_id not in (select pid from schedule where season = '2009 spring')
            and pa_id not in (select pid from availability where date = '2009-03-06' and unavailable=1 and season = '2009 spring')
            and pb_id not in (select pid from availability where date = '2009-03-06' and unavailable=1 and season = '2009 spring')
            and blockcouple = 1
            and couples.season = "2009 spring"
            ;
