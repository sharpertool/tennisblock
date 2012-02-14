<?php
// include shared code
include '../lib/common.php';
include '../lib/db.php';
include '../lib/functions.php';

// this should not be available unless the user has logged in 
include '401.php';

// insert a new blog entry
if ($_POST['post_id'] == 'new')
{
    $query = sprintf('INSERT INTO %sBLOG_POST SET POST_TITLE = "%s", ' .
        'POST_DATE = "%s", POST_TEXT = "%s"',
        DB_TBL_PREFIX,
        mysql_real_escape_string($_POST['post_title'], $GLOBALS['DB']),
        mysql_format_date($_POST['post_date']),
        mysql_real_escape_string($_POST['post_text'], $GLOBALS['DB']));
    
    mysql_query($query, $GLOBALS['DB']);
}
else
{
    // delete entry
    if (isset($_POST['delete']))
    {
        $query = sprintf('DELETE FROM %sBLOG_POST WHERE POST_ID = %d',
            DB_TBL_PREFIX, $_POST['post_id']);

        mysql_query($query, $GLOBALS['DB']);
    }
    // update entry
    else
    {
        $query = sprintf('UPDATE %sBLOG_POST SET POST_TITLE = "%s", ' .
            'POST_DATE = "%s", POST_TEXT = "%s" WHERE POST_ID = %d',
            DB_TBL_PREFIX,
            mysql_real_escape_string($_POST['post_title'], $GLOBALS['DB']),
            mysql_format_date($_POST['post_date']),
            mysql_real_escape_string($_POST['post_text'], $GLOBALS['DB']),
            $_POST['post_id']);
        
        mysql_query($query, $GLOBALS['DB']);
    }
}
mysql_close($GLOBALS['DB']);
header('Location: admin.php');
?>
