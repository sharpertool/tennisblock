<?php
// include shared code
include '../lib/config.php';

// make sure users only access files in the albums
$file = (isset($_GET['file'])) ? (BASEDIR . '/' . $_GET['file']) : '';
if ($file && strpos(realpath($file), BASEDIR) === 0 && file_exists($file))
{
    header('Content-Type: image/jpeg');
    // output thumbnail
    switch (substr($file, strrpos($file, '.') + 1))
    {
        // thumbnail is for jpeg image
        case 'jpg':
        case 'jpeg':
            include '../lib/JpegThumbnail.php';
            $thumbnail = new JpegThumbnail();
            imagejpeg($thumb = $thumbnail->generate($file), '', 100);
            imagedestroy($thumb);
            break;

        // thumbnail is for QuickTime video
        case 'mov':
            include '../lib/MovThumbnail.php';
            $thumbnail = new MovThumbnail();

            // get and determine dimensions of thumbnail image
            $thumb = $thumbnail->generate($file);
            $width = imagesx($thumb);
            $height = imagesy($thumb);
            
            // get and determine indicator dimensions
            $icon = imagecreatefromjpeg('overlay.jpg');
            $icon_width = imagesx($icon);
            $icon_height = imagesy($icon);
                    
            // copy indicator to lower right-hand corner of thumbnail
            imagecopymerge($thumb, $icon, $width - $icon_width, 
                $height - $icon_height, 0, 0, $icon_width, $icon_height, 100); 
            
            imagejpeg($thumb, '', 100);
            imagedestroy($thumb);
            imagedestroy($icon);
            break;
    }
}
?>


<?php
?>

