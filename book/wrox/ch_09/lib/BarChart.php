<?php
class BarChart
{
    private $width;   // width of chart
    private $height;  // height of chart
    private $image;   // image reference
    private $black;   // allocated color black

    // initialize new object
    public function __construct($width, $height)
    {
        // create new image
        $this->image = imagecreatetruecolor($width, $height);
        $this->width = $width;
        $this->height = $height;

        // fill image background white
        $white = imagecolorallocate($this->image, 0xFF, 0xFF, 0xFF);
        imagefill($this->image, 0,0, $white);

        // draw axis
        $this->black = imagecolorallocate($this->image, 0x00, 0x00, 0x00);
        imageline($this->image, 20, 0, 20, $height - 20, $this->black);
        imageline($this->image, 20, $height - 20, $width - 20, $height - 20,
            $this->black);
    }

    // dump image to browser or save
    public function flushImage($filename = '')
    {
        if ($filename)
        {
            imagepng($this->image, $filename);
        }
        else
        {
            header('Content-type: image/png');
            imagepng($this->image);
        }
    }

    // graph the data using the associated colors and labels
    public function graphData($data, $colors, $labels)
    {
        // start point
        $x = 20;
        $y = $this->height - 20;

        // calculate bar width
        $bar_width = ($this->width - $x - 20) / count($data);

        $ymax = max($data);

        foreach ($data as $i => $dat)
        {
            // calculate height of bar
            $bar_height = ($dat / $ymax) * ($this->height - 30);
            $color = imagecolorallocate($this->image, $colors[$i]['r'],
                $colors[$i]['g'], $colors[$i]['b']);

            // draw bar twice - once for filled area and again for outline
            imagefilledrectangle($this->image, $x, $y, $x + $bar_width,
                $y - $bar_height, $color);
            imagerectangle($this->image, $x, $y, $x + $bar_width,
                $y - $bar_height, $this->black);

            imagestring($this->image, 2, $x, $y, $labels[$i], $this->black);

            // increment starting point
            $x += $bar_width;
        }
    }
}
?>