<?php
// specify log file
define('LOGFILE', '/srv/apache/example.com/logs/database.log');

// define group and record separator characters
define('GS', chr(0x1D));
define('RS', chr(0x1E));

// begin or continue session
session_start();

// write the provided message to the log file
function write_log($message)
{
    $fp = fopen(LOGFILE, 'a');
    fwrite($fp, date('Ymd\THis') . $_SESSION['username'] . GS . $message . RS);
    fclose($fp);
}
?>
