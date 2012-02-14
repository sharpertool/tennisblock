<?php
include '../../lib/common.php';
include '../../lib/config.php';

// make sure we have all expected parameters
if (!isset($_POST['directory'])) return;

if ($_FILES['file']['error'])
{
    echo '<script type="text/javascript>parent.uploadFailed();</script>';
}
else
{
    // prevent users from traversing outside the base directory
    $directory = realpath(BASEDIR . $_POST['directory']);
    $target = $directory . '/' . $_FILES['file']['name'];

    if (move_uploaded_file($_FILES['file']['tmp_name'], $target))
    {
        echo '<script type="text/javascript">parent.uploadComplete();</script>';
    }
    else
    {
        echo '<script type="text/javascript">parent.uploadFailed();</script>';
    }
}
?>
