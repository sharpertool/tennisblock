<?php
// include shared code
include '../lib/common.php';
include '../lib/db.php';

// determine current viewed month and year
$timestamp = (isset($_GET['t'])) ? $_GET['t'] : time();
list($month, $year) = explode('/', date('m/Y', $timestamp));

// Javascript references
$GLOBALS['TEMPLATE']['extra_head'] = <<<ENDHTML
<script src="js/ajax.js" type="text/javascript"></script>
<script src="js/blog.js" type="text/javascript">
ENDHTML;

// retrieve entries for currently viewed month
$query = sprintf('
    SELECT
        POST_ID, POST_TITLE, POST_TEXT,
        UNIX_TIMESTAMP(POST_DATE) AS POST_DATE
    FROM
        %sBLOG_POST
    WHERE
        DATE(POST_DATE) BETWEEN
            "%d-%02d-01" AND 
            DATE("%d-%02d-01") + INTERVAL 1 MONTH - INTERVAL 1 DAY
    ORDER BY
        POST_DATE DESC',
    DB_TBL_PREFIX,
    $year,  $month,
    $year, $month);
$result = mysql_query($query, $GLOBALS['DB']);

ob_start();
while ($record = mysql_fetch_assoc($result))
{
    echo '<h2>' . $record['POST_TITLE'] . '</h2>';
    echo '<p>' . date('m/d/Y', $record['POST_DATE']) . '</p>';
    echo $record['POST_TEXT'];
    echo '<div style="display:none;" id="comments_' . $record['POST_ID'] .
        '"></div>';
    echo '<p><a href="#" onclick="toggleComments(' . $record['POST_ID'] . 
        ', this);return false;">Show Comments</a></p>';
    echo '<hr/>';
}
mysql_free_result($result);

// generate link to view previous month if appropriate
$query = sprintf('SELECT UNIX_TIMESTAMP(POST_DATE) AS POST_DATE ' .
    'FROM %sBLOG_POST ORDER BY POST_DATE DESC',
     DB_TBL_PREFIX);
$result = mysql_query($query, $GLOBALS['DB']);
if (mysql_num_rows($result))
{

    // determine date of newest post
    $row = mysql_fetch_assoc($result);
    $newest = $row['POST_DATE'];

    // determine date of oldest post
    mysql_data_seek($result, mysql_num_rows($result) - 1);
    $row = mysql_fetch_assoc($result);
    $oldest = $row['POST_DATE'];

    if ($timestamp > $oldest)
    {
        echo '<a href="' . htmlspecialchars($_SERVER['PHP_SELF']) .
            '?t=' . strtotime('-1 month', $timestamp) . '">Prev</a> ';
    }

    if ($timestamp < $newest)
    {
        echo ' <a href="' . htmlspecialchars($_SERVER['PHP_SELF']) .
            '?t=' . strtotime('+1 month', $timestamp) . '">Next</a>';
    }

}
mysql_free_result($result);

// link to RSS feed
$GLOBALS['TEMPLATE']['head_extra'] = '<link rel="alternate" ' . 
    'type="application/rss+xml"  href="rss.php" title="My Blog">';

echo '<p><a href="rss.php">RSS Feed</a></p>';
$GLOBALS['TEMPLATE']['content'] = ob_get_clean();


include '../templates/template-page.php';
mysql_close($GLOBALS['DB']);
?>
