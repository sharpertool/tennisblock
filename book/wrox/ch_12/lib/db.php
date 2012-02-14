<?php
// database connection and schema constants
define('DB_HOST', 'localhost');
define('DB_USER', 'TESTUSR');
define('DB_PASSWORD', 'TESTPASS');
define('DB_SCHEMA', 'TEST');
define('DB_TBL_PREFIX', 'WROX_');

// establish a connection to the database server
if (!$GLOBALS['DB'] = mysql_connect(DB_HOST, DB_USER, DB_PASSWORD))
{
    die('Error: Unable to connect to database server.');
}
if (!mysql_select_db(DB_SCHEMA, $GLOBALS['DB']))
{
    mysql_close($GLOBALS['DB']);
    die('Error: Unable to select database schema.');
}
?>
