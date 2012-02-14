<?php
function log_page_hit()
{
    $query = sprintf('INSERT INTO %sSITE_ACCESS (IP_ADDRESS, ' .
        'REQ_PAGE) VALUES ("%s", "%s")', DB_TBL_PREFIX,
        $_SERVER['REMOTE_ADDR'], 
        mysql_real_escape_string($_SERVER['SCRIPT_NAME'], $GLOBALS['DB']));

    return mysql_query($query, $GLOBALS['DB']);
}
?>
