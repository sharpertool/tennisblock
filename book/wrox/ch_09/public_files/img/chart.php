<?php
include '../../lib/common.php';
include '../../lib/db.php';
include '../../lib/BarChart.php';

// get current month and year
list($month, $year) = explode('/', date('m/Y'));

// determine which query to execute
if (isset($_GET['day']))
{
    // initialize arrays 
    $num_days = date("t", mktime(0, 0, 0, $month, 1, $year));
    for ($i = 1; $i < $num_days + 1; $i++)
    {
        $data[$i] = 0;
        $labels[$i] = $i;
        $colors[$i] = array('r' => 0xCC, 'g' => 0x33, 'b' => 0x33);
    }

    // retrieve total hits
    $query = sprintf('
        SELECT
            DAY(ACCESS_TIME) AS ATIME, COUNT(IP_ADDRESS) AS TOTAL
        FROM
            %sSITE_ACCESS
        WHERE
            DATE(ACCESS_TIME) BETWEEN
                "%d-%02d-01" AND
                "%d-%02d-01" + INTERVAL 1 MONTH - INTERVAL 1 DAY
        GROUP BY
            ATIME
        ORDER BY 
            ATIME ASC',
        DB_TBL_PREFIX,
        $year,
        $month,
        $year,
        $month);
        
    $result = mysql_query($query, $GLOBALS['DB']);
    while ($row = mysql_fetch_assoc($result))
    {
        $data[$row['ATIME']] = $row['TOTAL'];
    }
    mysql_free_result($result);
}
else if (isset($_GET['month']))
{
    // initialize arrays 
    for ($i = 1; $i < 13; $i++)
    {
        $data[$i] = 0;
        $labels[$i] = date("M", mktime(0,0,0,$i));
        $colors[$i] = array('r' => 0xCC, 'g' => 0x33, 'b' => 0x33);
    }        

    // retrieve total hits
    $query = sprintf('
        SELECT
            MONTH(ACCESS_TIME) AS ATIME, COUNT(IP_ADDRESS) AS TOTAL
        FROM
            %sSITE_ACCESS
        WHERE  
            DATE(ACCESS_TIME) BETWEEN
                "%d-01-01" AND
                "%d-12-31"
            GROUP
                BY ATIME
            ORDER BY
                ATIME ASC',
            DB_TBL_PREFIX,
            $year,
            $year);
    $result = mysql_query($query, $GLOBALS['DB']);

    while ($row = mysql_fetch_assoc($result))
    {
        $data[$row['ATIME']] = $row['TOTAL'];
    }
    mysql_free_result($result);
}
else
{
    die();
}

// present bar chart
$chart = new BarChart(500, 200);
$chart->graphData($data, $colors, $labels);
$chart->flushImage();
?>
