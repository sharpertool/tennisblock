<?php
// include shared code
include '../lib/common.php';
include '../lib/db.php';

// user should be logged in 
include '401.php';

// retrieve blog entry content
$query = sprintf('SELECT POST_ID, POST_TITLE, POST_TEXT, ' .
    'UNIX_TIMESTAMP(POST_DATE) AS POST_DATE FROM %sBLOG_POST WHERE ' .
    'POST_ID = "%d"',
    DB_TBL_PREFIX, $_GET['post_id']);
$result = mysql_query($query, $GLOBALS['DB']);
$record = mysql_fetch_assoc($result);

// output blog entry
$data = array(
	'post_id' => $record['POST_ID'],
	'post_title' => $record['POST_TITLE'],
	'post_text' => $record['POST_TEXT'],
	'post_date' => date('m/d/Y', $record['POST_DATE']));
echo json_encode($data);

mysql_free_result($result);
mysql_close($GLOBALS['DB']);
?>
