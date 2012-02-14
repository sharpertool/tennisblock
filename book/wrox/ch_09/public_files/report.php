<?php
include '../lib/common.php';
include '../lib/db.php'; 

// determine useful date values
list($full_month, $full_year, $short_month, $num_month, $short_year) =
    explode('/', date('F/Y/M/m/y'));
?>
<html>
 <head>
  <title>Website Statistics</title>
  <style type="text/css">
table {
    border-collapse: collapse;
}
th.blank {
    border: none;
}
th, td {
    text-align: center;
    vertical-align: top;
    border: 1px solid black;
    padding: 4px;
}
th.label {
    text-align: right;
}
  </style>
 </head>
 <body>
  <h1>Website Statistics</h1>
  <table>
   <tr>
    <th class="blank"> </th>
    <th>Current Month (<?php echo $short_month . ' ' . $short_year; ?>)</th>
    <th>Year to Date</th></th>
   </tr>
<?php
// retrieve the unique IP addresses for the current month
$query = sprintf('
    SELECT
        INET_NTOA(IP_ADDRESS) AS IP_ADDRESS
    FROM 
        %sSITE_ACCESS SA
    WHERE
        DATE(ACCESS_TIME) BETWEEN
            "%d-%02d-01" AND  
            "%d-%02d-01" + INTERVAL 1 MONTH - INTERVAL 1 DAY
    GROUP BY
        SA.IP_ADDRESS
    ORDER BY
        COUNT(IP_ADDRESS) DESC',
    DB_TBL_PREFIX,
    $full_year,
    $num_month,
    $full_year,
    $num_month);
$result = mysql_query($query, $GLOBALS['DB']);

// total addresses
$mo_total = mysql_num_rows($result);

// collect the top 10 IP addresses from the result set
for ($i = 0; $i < 10 && $i < $mo_total; $i++)
{
    $row = mysql_fetch_assoc($result);
    $mo_addrs[] = $row['IP_ADDRESS'];
}
mysql_free_result($result);

// retrieve the unique IP addresses for the current year
$query = sprintf('
    SELECT
        INET_NTOA(IP_ADDRESS) AS IP_ADDRESS 
    FROM 
        %sSITE_ACCESS
    WHERE
        DATE(ACCESS_TIME) BETWEEN
            "%d-01-01" AND 
            "%d-01-01" + INTERVAL 1 YEAR - INTERVAL 1 DAY
    GROUP BY
        IP_ADDRESS 
    ORDER BY
        COUNT(IP_ADDRESS) DESC',
    DB_TBL_PREFIX,
    $full_year,
    $full_year);
$result = mysql_query($query, $GLOBALS['DB']);

// total addresses
$yr_total = mysql_num_rows($result);

// collect the top 10 IP addresses from the result set
for ($i = 0; $i < 10 && $i < $yr_total; $i++)
{
    $row = mysql_fetch_assoc($result);
    $yr_addrs[] = $row['IP_ADDRESS'];
}
mysql_free_result($result);
?>
   <tr>
    <th class="label">Unique Visitors</th>
    <td><?php echo $mo_total;?></td>
    <td><?php echo $yr_total;?></td>
   </tr><tr>
    <th class="label">Top 10 IP Addresses</th>
    <td><?php foreach ($mo_addrs as $addr) echo $addr . '<br/>';?></td>
    <td><?php foreach ($yr_addrs as $addr) echo $addr . '<br/>';?></td>
   </tr>
<?php
// retrieve the top 5 pages accessed during the current month
$query = sprintf('
    SELECT
        REQ_PAGE, COUNT(REQ_PAGE) AS TOTAL
    FROM
        %sSITE_ACCESS
    WHERE
        DATE(ACCESS_TIME) BETWEEN
            "%d-%02d-01" AND
            "%d-%02d-01" + INTERVAL 1 MONTH - INTERVAL 1 DAY
    GROUP BY
        REQ_PAGE 
    ORDER BY
        TOTAL DESC
    LIMIT 5',
    DB_TBL_PREFIX,
    $full_year,
    $num_month, 
    $full_year,
    $num_month);
$result = mysql_query($query, $GLOBALS['DB']);

// collect the pages from the result set
while ($row = mysql_fetch_assoc($result))
{
    $mo_pages_most[] = $row['REQ_PAGE'];
}
mysql_free_result($result);

// retrieve the top 5 pages accessed during the current year
$query = sprintf('
    SELECT
        REQ_PAGE, COUNT(REQ_PAGE) AS TOTAL
    FROM
        %sSITE_ACCESS
    WHERE
        DATE(ACCESS_TIME) BETWEEN
            "%d-01-01" AND  
            "%d-01-01" + INTERVAL 1 YEAR - INTERVAL 1 DAY
    GROUP BY
        REQ_PAGE
    ORDER BY
        TOTAL DESC
    LIMIT 5',
    DB_TBL_PREFIX,
    $full_year,
    $full_year);
$result = mysql_query($query, $GLOBALS['DB']);

// collect the pages from the result set
while ($row = mysql_fetch_assoc($result))
{
    $yr_pages_most[] = $row['REQ_PAGE'];
}
mysql_free_result($result);
?>
   <tr>
    <th class="label">Top 5 Most Popular Pages</th>
    <td><?php foreach ($mo_pages_most as $addr) echo $addr . '<br/>';?></td>
    <td><?php foreach ($yr_pages_most as $addr) echo $addr . '<br/>';?></td>
   </tr>
<?php
// reverse sort order to retrieve the 5 least popular pages
$query = sprintf('
    SELECT
        REQ_PAGE, COUNT(REQ_PAGE) AS TOTAL
    FROM
        %sSITE_ACCESS
    WHERE
        DATE(ACCESS_TIME) BETWEEN
            "%d-%02d-01" AND 
            "%d-%02d-01" + INTERVAL 1 MONTH - INTERVAL 1 DAY
    GROUP BY
        REQ_PAGE
    ORDER BY
        TOTAL ASC
    LIMIT 5',
    DB_TBL_PREFIX,
    $full_year,
    $num_month,
    $full_year,
    $num_month);
$result = mysql_query($query, $GLOBALS['DB']);

// collect the least popular pages from the result set
while ($row = mysql_fetch_assoc($result))
{
    $mo_pages_least[] = $row['REQ_PAGE'];
}
mysql_free_result($result);

$query = sprintf('
    SELECT
        REQ_PAGE, COUNT(REQ_PAGE) AS TOTAL
    FROM
        %sSITE_ACCESS
    WHERE
        DATE(ACCESS_TIME) BETWEEN
            "%d-01-01" AND
            "%d-01-01" + INTERVAL 1 YEAR - INTERVAL 1 DAY
    GROUP BY
        REQ_PAGE 
    ORDER BY
        TOTAL ASC
    LIMIT 5',
    DB_TBL_PREFIX,
    $full_year,
    $full_year);
$result = mysql_query($query, $GLOBALS['DB']);

// collect the least popular pages
while ($row = mysql_fetch_assoc($result))
{
    $yr_pages_least[] = $row['REQ_PAGE'];
}
mysql_free_result($result);
?>
   <tr>
    <th class="label">Top 5 Least Popular Pages</th>
    <td><?php foreach ($mo_pages_least as $addr) echo $addr . '<br/>';?></td>
    <td><?php foreach ($yr_pages_least as $addr) echo $addr . '<br/>';?></td>
   </tr>
  </table>

  <p><strong>Monthly Traffic Distribution for
   <?php echo $full_year; ?></strong></p>
  <p><img src="img/chart.php?month" alt="monthly traffic distribution"></p>
  
  <p><strong>Daily Traffic Distribution for <?php echo $full_month . ' ' .
    $full_year; ?></strong></p>
  <p><img src="img/chart.php?day" alt="daily traffic distribution"></p>
 </body>
</html>
