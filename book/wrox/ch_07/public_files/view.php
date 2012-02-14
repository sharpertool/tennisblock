<?php
// include shared code
include '../lib/config.php';

// make sure users only access files in the albums
$file = (isset($_GET['file'])) ? (BASEDIR . '/' . $_GET['file']) : '';
if ($file && strpos(realpath($file), BASEDIR) === 0 && file_exists($file))
{
    // dump file content to browser
    switch(substr($file, strrpos($file, '.') + 1))
    {
        // file is jpeg image
        case 'jpg':
        case 'jpeg':
            header('Content-Type: image/jpeg');
            readfile($file);
            break;

        // file is quicktime movie
        case 'mov':
            header('Content-Type: movie/quicktime');
            readfile($file);
    }
}
?>
