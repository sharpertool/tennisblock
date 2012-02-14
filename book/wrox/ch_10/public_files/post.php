<?php
// include shared code
include '../lib/common.php';
include '../lib/db.php';

// validate incoming values
$name = (isset($_POST['person_name'])) ? trim($_POST['person_name']) : '';
$comment = (isset($_POST['post_comment'])) ? trim($_POST['post_comment']) : '';

if ($name && $comment)
{
    // add comment
    $query = sprintf('INSERT INTO %sBLOG_COMMENT (POST_ID, PERSON_NAME, ' .
        'POST_COMMENT) VALUES (%d, "%s", "%s")',
        DB_TBL_PREFIX,
        $_GET['id'],
        htmlspecialchars($name),
        htmlspecialchars($comment));
    mysql_query($query, $GLOBALS['DB']);
    echo 'OK';
}
else
{
    echo 'ERR';
}
mysql_close($GLOBALS['DB']);
?>
