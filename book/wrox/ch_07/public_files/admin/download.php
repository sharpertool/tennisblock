<?php
include '../../lib/common.php';
include '../../lib/config.php';


$dir = $_GET['dir'];
$file = $_GET['file'];

$target = BASEDIR . $dir . '/' . $file;

if (file_exists($target) && is_file($target))
{
    header('Content-Type: application/force-download');
    header('Content-Disposition: attachment; filename="' . $file . '";');
    header('Content-Transfer-Encoding: binary');
    header('Content-Length: ' . filesize($target));
    readfile($target);
}
?>
