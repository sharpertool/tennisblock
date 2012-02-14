<?php
include '../lib/common.php';
include '../lib/db.php';
include '401.php';

// generate extra elements for HTML head section
ob_start();
?>
<script type="text/javascript" src="js/yui/yahoo-dom-event/yahoo-dom-event.js">
</script>
<script type="text/javascript" src="js/yui/calendar/calendar-min.js"></script>
<script type="text/javascript" src="js/tinymce/tiny_mce.js"></script>
<script type="text/javascript" src="js/helper.js"></script>
<script type="text/javascript" src="js/blog_admin.js"></script>

<script type="text/javascript">
   tinyMCE.init({mode : "textareas", theme : "simple", width : "450" });
</script>
<link rel="stylesheet" type="text/css" href="css/calendar.css" />
<style type="text/css">
#calendar {
    display: none;
    position: absolute;
    z-index: 1;
}
</style>
<?php
$GLOBALS['TEMPLATE']['extra_head'] = ob_get_contents();
ob_clean();

// Generate entry form
?>
<form action="post_admin.php"
 method="post">
 <div id="form_select">
  <table>
   <tr>
    <td class="label"><label for="post_id">Blog Post</label></td>
    <td>
     <select name="post_id" id="post_id"/>
      <option value="select">SELECT</option>
      <option value="new">Add New</option>
<?php
// retrieve list of post titles
$query = sprintf('SELECT POST_ID, POST_TITLE, UNIX_TIMESTAMP(POST_DATE) ' .
    'AS POST_DATE FROM %sBLOG_POST ORDER BY POST_DATE DESC, POST_TITLE ASC',
    DB_TBL_PREFIX);

$result = mysql_query($query, $GLOBALS['DB']);
while ($record = mysql_fetch_assoc($result))
{
    echo '<option value="' . $record['POST_ID'] . '">';
    echo '(' . date('m/d/Y', $record['POST_DATE']) . ') ' .
        $record['POST_TITLE'];
    echo '</option>';
}
mysql_free_result($result);
?>
     </select>
    </td>
   </tr>
  </table>
 </div>
 <div id="form_fields" style="display:none;">
  <table>
   <tr>
    <td class="label"><label for="post_title">Title</label></td>
    <td><input type="text" name="post_title" id="post_title"/></td>
   </tr><tr>
    <td class="label"><label for="post_date">Date</label></td>
    <td class="yui-skin-sam"><input type="text" name="post_date" id="post_date"
     maxlength="10" size="10" value="<?php echo date('m/d/Y'); ?>"/>
     <img id="show_calendar" src="img/calendar.jpg" alt="Show Calendar" />
     <div id="calendar"></div> 
</td>
   </tr><tr>
    <td class="label"><label for=news_content">Content</label></td>
    <td>
     <textarea id="post_text" name="post_text" rows="15" cols="60"></textarea>
    </td>
   </tr><tr id="delete_field">
    <td> </td>
    <td style="text-align: right;">
     <input type="checkbox" id="delete" name="delete"/>
     <label for="delete">Delete Entry</label></td>
   </tr><tr>
    <td> </td>
    <td>
     <input type="submit" value="Submit" id="form_submit" class="button"/>
     <input type="reset" value="Cancel" id="form_reset" class="button"/></td>
   </tr>
  </table>
 </div>
</form>
<?php
$GLOBALS['TEMPLATE']['content'] = ob_get_clean();

include '../templates/template-page.php';
mysql_close($GLOBALS['DB']);
?>
