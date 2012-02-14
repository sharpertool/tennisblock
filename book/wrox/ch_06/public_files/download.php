<?php
include '../lib/common.php';
include '../lib/config.php';

// prevent users from traversing outside the base directory
$dir = BASEDIR . $_POST['dir'];
$target = realpath($dir . '/' . $_GET['file']);
if (strpos($target, BASEDIR) !== 0)
{
    die();
}

// send the file if it exists
if (file_exists($target) && is_file($target))
{
    header('Content-Type: application/force-download');
    header('Content-Disposition: attachment; filename="' .
        $_GET['file'] . '";');
    header('Content-Transfer-Encoding: binary');
    header('Content-Length: ' . filesize($target));
    readfile($target);
}
?>
