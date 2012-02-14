<?php
define('SOI', pack('n', 0xFFD8));  // jpeg start marker
define('EOI', pack('n', 0xFFD9));  // jpeg end marker

class MovThumbnail
{
    public $width;  // maximum thumbnail width
    public $height; // maximum thumbnail height

    // initialize a new MovThumbnail object
    public function __construct($width = 100, $height = 100)
    {
        $this->width = $width;
        $this->height = $height;
    }
    
    // accept a source file location and return an open image handle or
    // save to disk if destination provided 
    public function generate($src, $dest = '')
    {
        // locate the first SOI marker
        for (
          $fp = fopen($src, 'rb'), $bytes = null;
          $bytes != SOI && !feof($fp);
          $bytes = fread($fp, 2)
        );

        // extract jepg image
        for (
          $buffer = $bytes;
          $bytes != EOI && !feof($fp);
          $bytes = fread($fp, 2), $buffer .= $bytes
        );

        // construct image from buffer
        $img = imagecreatefromstring($buffer);

        // retrieve image dimensions
        $width = imagesx($img);
        $height = imagesy($img);

        // determine if resize is necessary
        if(($lowest = min($this->width / $width, $this->height / $height)) < 1)
        {
            // resize
            $sm_width = floor($lowest * $width);
            $sm_height = floor($lowest * $height);
            $buffer = imagecreatetruecolor($sm_width, $sm_height);
            imagecopyresized($buffer, $img, 0,0, 0,0, $sm_width, $sm_height,
                $width, $height);
            imagedestroy($img);
            $img = $buffer;
        }
        
        // save to disk or return the open image handle
        if ($dest)
        {
            imagejpeg($img, $dest, 100);
            imagedestroy($img);
        }
        else
        {
            return $img;
        }
    }
}
?>