<?php
/**
 *=-----------------------------------------------------------=
 * Season.php
 *=-----------------------------------------------------------=
 * Author: Ed Henderson
 *
 * The Season class contains Season information
 */
require_once('../inc/dbmanager.php');

class Season
{
    public $sid;
    public $season;
    public $courts;
    public $firstcourt;
    
    public function __construct($dbrow = null)
    {
        if ($dbrow != NULL) {
            if (array_key_exists('id',$dbrow)){
                $this->sid    = $dbrow['id'];
            }
            $this->season       = $dbrow['name'];
            $this->courts       = $dbrow['courts'];
            $this->firstcourt   = $dbrow['firstcourt'];
        }
    }
    
}

?>
