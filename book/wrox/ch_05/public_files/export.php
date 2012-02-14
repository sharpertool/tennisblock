<?php
include '../lib/common.php';
include '../lib/db.php';

define('CRLF', "\r\n");

// retrieve all events
$query = sprintf('SELECT EVENT_NAME, UNIX_TIMESTAMP(EVENT_TSTAMP) AS ' . 
    'EVENT_TSTAMP, NOTIFY FROM %sCALENDAR ORDER BY EVENT_TSTAMP ASC, ' . 
    'EVENT_NAME ASC',
    DB_TBL_PREFIX);
$result = mysql_query($query, $GLOBALS['DB']);

// generate iCalendar
ob_start();
echo 'BEGIN:VCALENDAR' . CRLF;
echo 'PRODID:-//Wrox//PHP Reuse//EN' . CRLF;
echo 'VERSION:2.0' . CRLF;

while ($row = mysql_fetch_assoc($result))
{
    echo 'BEGIN:VEVENT' . CRLF;
    echo 'DTSTART:' . date('Ymd\THis', $row['EVENT_TSTAMP']) . CRLF;
    echo 'DTEND:' . date('Ymd\THis', strtotime('+30 minutes',
        $row['EVENT_TSTAMP'])) . CRLF;
    echo 'SUMMARY:' . htmlspecialchars($row['EVENT_NAME']) . CRLF;
    if ($row['NOTIFY'])
    {
        echo 'BEGIN:VALARM' . CRLF;
        echo 'ACTION:DISPLAY' . CRLF;
        echo 'SUMMARY:' . date('m/d/Y H:i A - ', $row['EVENT_TSTAMP']) . 
            htmlspecialchars($row['EVENT_NAME']) . CRLF;
        echo 'TRIGGER:-PT60M' . CRLF;
        echo 'END:VALARM' . CRLF;
    }
    echo 'END:VEVENT' . CRLF;
}
mysql_free_result($result);

echo 'END:VCALENDAR' . CRLF;
$ics = ob_get_clean();
// send iCalendar file to browser
header('Content-Type: text/calendar');
header('Content-Disposition: attachment; filename="export.ics";');
header('Content-Transfer-Encoding: binary');
header('Content-Length: ' . strlen($ics));
echo $ics;

mysql_close($GLOBALS['DB']);
?>
