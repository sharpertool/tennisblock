<?php
// include shared code
include '../lib/common.php';
include '../lib/db.php';

// retrieve comments for this post
$id = (int)$_GET['post_id'];
$query = sprintf('SELECT PERSON_NAME, POST_COMMENT, ' .
    'UNIX_TIMESTAMP(COMMENT_DATE) AS COMMENT_DATE FROM %sBLOG_COMMENT ' .
    'WHERE POST_ID = %d ORDER BY COMMENT_DATE ASC',
    DB_TBL_PREFIX, $id);
$result = mysql_query($query, $GLOBALS['DB']);

if (mysql_num_rows($result))
{
    while($row = mysql_fetch_assoc($result))
    {
        echo '<p>' . htmlspecialchars($row['POST_COMMENT']) . '<br/>';
        echo htmlspecialchars($row['PERSON_NAME']) . ' ' . 
            date('m/d/Y', $row['COMMENT_DATE']) . '</p>';
    }
}
else
{
    echo '<p>There are no comments for this post.</p>';
}

// form to add comments
?>
<form action="post.php?id=<?php echo $id; ?>" method="post"
onsubmit="postComment(<?php echo $id; ?>, this); return false;">
<div>
 <label for="name_<?php echo $id; ?>">Name: </label>
 <input type="text" name="person_name" id="name_<?php echo $id; ?>"/><br />
 <label for="comment_<?php echo $id; ?>">Comment: </label>
 <textarea type="text" name="post_comment" 
  id="comment_<?php echo $id; ?>"/></textarea></br>
 <input type="submit" value="submit" />
</form>

<?php
mysql_free_result($result);
mysql_close($GLOBALS['DB']);
?>
