<?php
include '../lib/common.php';
include '../lib/config.php';

// make sure we have all expected parameters
if (!isset($_POST['directory'])) return;

// the file uploaded successfully
if (!$_FILES['file']['error'])
{
    // prevent users from traversing outside the base directory
    $dir = realpath(BASEDIR . $_POST['dir']);
    $target = BASEDIR . $dir . '/' . $_FILES['file']['name'];
    if (strpos($target, BASEDIR) !== 0)
    {
        echo '<script type="text/javascript">parent.uploadFailed();</script>';
        die();
    }

    // must move the file to a permanent location
    if (move_uploaded_file($_FILES['file']['tmp_name'], $target))
    {
        echo '<script type="text/javascript">parent.refreshFilesList();' .
            '</script>';
    }
    else
    {
        // there was a problem moving the file
        echo '<script type="text/javascript">parent.uploadFailed();</script>';
    }
}
// there was a problem uploading the file
else
{
    echo '<script type="text/javascript">parent.uploadFailed();</script>';
}
?>
