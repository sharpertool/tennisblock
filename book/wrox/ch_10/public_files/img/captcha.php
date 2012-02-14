<?php
include '../../lib/functions.php';

// must start or continue session and save captcha string in $_SESSION for it
// to be available to other requests
session_start();

// create a 65x20 pixel image
$image = imagecreate(65, 20);

// fill the image background color
$bg_color = imagecolorallocate($image, 51, 102, 255);
imagefilledrectangle($image, 0, 0, 65, 20, $bg_color);

// fetch random text
$text = random_text(5);

// determine x and y coordinates for centered text
$font = 5;
$x = imagesx($image) / 2 - strlen($text) * imagefontwidth($font) / 2;
$y = imagesy($image) / 2 - imagefontheight($font) / 2;

// write text
$fg_color = imagecolorallocate($image, 255, 255, 255);
imagestring($image, $font, $x, $y, $text, $fg_color);
 
// save the captcha text to compare later
$_SESSION['captcha'] = $text;

// output the image
header('Content-type: image/png');
imagepng($image);
imagedestroy($image);
?>
