<?php
// specify log file
define('LOGFILE', 'database.log');

// define group and record separator characters
define('GS', chr(0x1D));
define('RS', chr(0x1E));

$fp = fopen(LOGFILE, 'r');

echo '<pre>';
// read in record until the record separator is encountered
while (!feof($fp))
{
    $c = '';
    $line = '';
    while ($c != RS && !feof($fp))
    {
        $line .= $c = fgetc($fp);
    }

    // split the line on the group separator
    $tmp = explode(GS, $line);

    $record = array();

    // timestamp is 15-characters long, the remaining is username
    $record['timestamp'] = substr($tmp[0], 0, 15);
    $record['username'] = htmlspecialchars(substr($tmp[0], 15));

    $record['message'] = htmlspecialchars($tmp[1]);
    
    print_r($record);
}
fclose($fp);

echo '</pre>';
?>

