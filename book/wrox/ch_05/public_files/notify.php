<?php
include '../lib/common.php';
include '../lib/db.php';

// the email address that will receive reminders
define('EMAIL_ADDR', 'tboronczyk@gmail.com);

// determine the current date and time values
list($month, $day, $year, $hour, $minute, $am) = explode('/',
    date('m/d/Y/G/i/A'));

// retrieve upcoming events
$query = sprintf('SELECT EVENT_NAME, UNIX_TIMESTAMP(EVENT_TSTAMP) AS ' . 
    'EVENT_TSTAMP FROM %sCALENDAR WHERE NOTIFY = 1 AND EVENT_TSTAMP BETWEEN ' .
    '"%4d-%02d-%02d %02d:%02d:00" AND "%4d-%02d-%02d %02d:%02d:00" ORDER BY ' .
    'EVENT_TSTAMP ASC, EVENT_NAME ASC',
     DB_TBL_PREFIX,
     $year, $month, $day, $hour, $minute,
     $year, $month, $day, $hour, $minute + 15);

$result = mysql_query($query, $GLOBALS['DB']);
if (mysql_num_rows($result))
{
    // construct the reminder message    
    $msg = 'Don\'t forget!  You have the following events scheduled:' . "\n\n";
    while ($row = mysql_fetch_assoc($result))
    {
        $msg .= '  * ' . date('h:i A - ', $row['EVENT_TSTAMP']) . 
            $row['EVENT_NAME'] . "\n";
    }

    // send the message
    mail(EMAIL_ADDR, "Reminders for $month/$day/$year $hour:$minute $am", $mgs);  
}
mysql_free_result($result);
mysql_close($GLOBALS['DB']);
?>
