<?php
class PieChart
{
    private $center;  // center point
    private $width;   // width of chart
    private $image;   // image reference

    // initialize new object
    public function __construct($width)
    {
        // create a new image
        $this->image = imagecreatetruecolor($width, $width);

        // determine center of image
        $this->center = $width / 2;
        $this->width = $width;

        // fill image background white
        $white = imagecolorallocate($this->image, 0xFF, 0xFF, 0xFF);
        imagefill($this->image, 0,0, $white);
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

    // graph the data using the associated colors
    public function graphData($data, $colors)
    {
        // allocate black for slice outline
        $black = imagecolorallocate($this->image, 0x00, 0x00, 0x00);
    
        // sum of all values
        $sum = array_sum($data);
    
        // starting angle of pie slice
        $start = -90;
    
        for ($i = 0; $i < count($data); $i++)
        {
            $color = imagecolorallocate($this->image, $colors[$i]['r'],
                $colors[$i]['g'], $colors[$i]['b']);
    
            // stop angle of pie slice
            $stop = (100 * $data[$i] / $sum * 3.6) + $start;
    
            // draw arc twice - once for filled area and again for outline
            imagefilledarc($this->image, $this->center, $this->center,
                $this->width, $this->width, $start, $stop, $color,
                IMG_ARC_PIE);
            imagefilledarc($this->image, $this->center, $this->center,
                $this->width, $this->width, $start, $stop, $black,
                IMG_ARC_NOFILL | IMG_ARC_EDGED);
    
            // increment to next starting point
            $start = $stop;
        }
    }
}

$data = array(150, 302, 250);
$colors = array(
    array('r' => 0x33, 'g' => 0xCC, 'b' => 0xFF),
    array('r' => 0xFF, 'g' => 0x33, 'b' => 0xCC),
    array('r' => 0xCC, 'g' => 0xFF, 'b' => 0x33));

$chart = new PieChart(150);
$chart->graphData($data, $colors);
$chart->flushImage();
?>