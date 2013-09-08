select
    concat(p1.firstname," ",p1.lastname) p1_name,
    concat(p2.firstname," ",p2.lastname) p2_name,
    concat(p3.firstname," ",p3.lastname) p3_name,
    concat(p4.firstname," ",p4.lastname) p4_name,
    
    concat(p5.firstname," ",p5.lastname) p5_name,
    concat(p6.firstname," ",p6.lastname) p6_name,
    concat(p7.firstname," ",p7.lastname) p7_name,
    concat(p8.firstname," ",p8.lastname) p8_name,

    concat(p9.firstname," ",p9.lastname) p9_name,
    concat(p10.firstname," ",p10.lastname) p10_name,
    concat(p11.firstname," ",p11.lastname) p11_name,
    concat(p12.firstname," ",p12.lastname) p12_name,
    
    truncate(abs((p1.NTRP+p2.NTRP)-(p3.NTRP+p4.NTRP)),2) d1_ntrp,
    truncate(abs((p5.NTRP+p6.NTRP)-(p7.NTRP+p8.NTRP)),2) d2_ntrp,
    truncate(abs((p9.NTRP+p10.NTRP)-(p11.NTRP+p12.NTRP)),2) d3_ntrp,
    truncate(abs((p1.microNTRP+p2.microNTRP)-(p3.microNTRP+p4.microNTRP)),2) d1_untrp,
    truncate(abs((p5.microNTRP+p6.microNTRP)-(p7.microNTRP+p8.microNTRP)),2) d2_untrp,
    truncate(abs((p9.microNTRP+p10.microNTRP)-(p11.microNTRP+p12.microNTRP)),2) d3_untrp
    ,truncate(abs((p1.NTRP+p2.NTRP)-(p3.NTRP+p4.NTRP))+abs((p5.NTRP+p6.NTRP)-(p7.NTRP+p8.NTRP))+abs((p9.NTRP+p10.NTRP)-(p11.NTRP+p12.NTRP)),2) sum_diff
    ,truncate(abs((p1.microNTRP+p2.microNTRP)-(p3.microNTRP+p4.microNTRP))+abs((p5.microNTRP+p6.microNTRP)-(p7.microNTRP+p8.microNTRP))+abs((p9.microNTRP+p10.microNTRP)-(p11.microNTRP+p12.microNTRP)),2) sum_udiff
    #max(abs((p1.NTRP+p2.NTRP)-(p3.NTRP+p4.NTRP)),abs((p5.NTRP+p6.NTRP)-(p7.NTRP+p8.NTRP)),abs((p9.NTRP+p10.NTRP)-(p11.NTRP+p12.NTRP))) maxd,
    #,sum(d1_ntrp,d2_ntrp,d3_ntrp)
    
from 
    tmp_sets,
    players p1,
    players p2,
    players p3,
    players p4,
    players p5,
    players p6,
    players p7,
    players p8,
    players p9,
    players p10,
    players p11,
    players p12

where
    1
    and m1_m1_pid = p1.pid
    and m1_f1_pid = p2.pid
    and m1_m2_pid = p3.pid
    and m1_f2_pid = p4.pid
    and m2_m1_pid = p5.pid
    and m2_f1_pid = p6.pid
    and m2_m2_pid = p7.pid
    and m2_f2_pid = p8.pid
    and m3_m1_pid = p9.pid
    and m3_f1_pid = p10.pid
    and m3_m2_pid = p11.pid
    and m3_f2_pid = p12.pid
    
order by sum_udiff
limit 100
    
