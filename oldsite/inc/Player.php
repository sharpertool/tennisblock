<?php
/**
 *=-----------------------------------------------------------=
 * ScheduleManager.inc
 *=-----------------------------------------------------------=
 * Author: Ed Henderson
 *
 * The ScheduleManger class is responsible for updating, and
 * manipulationg scedules
 */
require_once('../inc/dbmanager.php');

class Player
{
    public $pid;
    public $firstname;
    public $lastname;
    public $NTRP;
    public $uNTRP;
    public $gender;
    public $unavailable;
    
    # This is not a good encapsulation..
    # But it is easier to add this here then to change everything else.. so, for now,
    # I'll add it. It will only be set when this player is scheduled with a particular id.
    public $schedid;

    public function __construct($dbrow = null)
    {
        if ($dbrow != NULL) {
            if (array_key_exists('pid',$dbrow)){
                $this->pid        = $dbrow['pid'];
            }
            $this->firstname  = $dbrow['firstname'];
            $this->lastname   = $dbrow['lastname'];
            $this->NTRP       = $dbrow['NTRP'];
            $this->uNTRP      = $dbrow['microNTRP'];
            $this->gender     = $dbrow['gender'];
            if (array_key_exists('email',$dbrow)) {
                $this->email = $dbrow['email'];
            }
            if (array_key_exists('home',$dbrow)) {
                $this->home = $dbrow['home'];
            }
            if (array_key_exists('cell',$dbrow)) {
                $this->cell = $dbrow['cell'];
            }
            if (array_key_exists('work',$dbrow)) {
                $this->work = $dbrow['work'];
            }
            if (array_key_exists('schedid',$dbrow)) {
                $this->schedid = $dbrow['schedid'];
            }
        }
        $this->unavailable = array();
    }
    
    public function getName() {
        return sprintf("%s %s",$this->firstname,$this->lastname);
    }
    
    public static function getPlayer($pid) {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        /**
        * Build a query to ask if there is any overlap.
        */
        $query =
            "select " .
            "   pid, firstname, lastname, NTRP, microNTRP, gender, email, home, cell, work " .
            "from players " .
            "where pid = $pid";

        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);
        
        $player = NULL;
        if ($results->num_rows == 1)
        {
            $in = @$results->fetch_assoc();
            $player = new Player($in);
        }
        $results->close();
        return $player;
    }
    
    public function isAvailable($date)
    {
        # Incoming is a Unix date.
        $d = date("Y-m-d",$date);
        if (array_key_exists($d,$this->unavailable) and $this->unavailable[$d]) {
            return False;
        }
        return True;
    }
    
    public function isScheduled($date)
    {
        # Incoming is a Unix date.
        $d = date("Y-m-d",$date);
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        $pid = $this->pid;
        /**
        * Build a query to ask if there is any overlap.
        */
        $query = <<<EOQUERY
        SELECT
            count(*) cnt
        from
            blockmeetings bm, schedule s
        where
            bm.meetid = s.matchid
            and bm.date = '$d'
            and s.pid = $pid
            ;
EOQUERY;


        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
            if ($results === FALSE or $results === NULL)
            throw new DatabaseErrorException($conn->error);
        

        $n = 0;
        
        while (($row = @$results->fetch_assoc()) != NULL) 
        {
            $n = $row['cnt'];
        }
        
        if ($n > 0) {
            return true;
        }
        return false;
    }
    
    public function updateAvailability()
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        /**
        * Build a query to ask if there is any overlap.
        */
        $query = <<<EOQUERY
        SELECT
            date, unavailable
        from
            availability
        where 
            pid = $this->pid
        order by date
            ;
EOQUERY;


        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
            if ($results === FALSE or $results === NULL)
            throw new DatabaseErrorException($conn->error);
        
        $output = NULL;
        while (($row = @$results->fetch_assoc()) != NULL) 
        {
            $date = $row['date'];
            $unavail = $row['unavailable'];
            $this->unavailable[$date] = $unavail;
        }
    }
}

class Couple
{
    public $coupleid;
    public $paid;
    public $pbid;
    public $name;
    public $fulltime;
    public $nplays;
    
    public function __construct($in = NULL)
    {
        if ($in != NULL) {
            if (is_array($in)) {
              $this->coupleid     = $in['coupleid'];
              $this->paid         = $in['pa_id'];
              $this->pbid         = $in['pb_id'];
              $this->name         = $in['couplename'];
              $this->fulltime     = $in['fulltime'];
            } else if (is_numeric($in)) {
                $conn = DBManager::getConnection();
                $query = "select * from couples where coupleid = $in";
                $results = @$conn->query($query);
                if ($results === FALSE or $results === NULL)
                  throw new DatabaseErrorException($conn->error);
                
                if ($results->num_rows == 1)
                {
                    $in = @$results->fetch_assoc();
                    $this->coupleid     = $in['coupleid'];
                    $this->paid         = $in['pa_id'];
                    $this->pbid         = $in['pb_id'];
                    $this->name         = $in['couplename'];
                    $this->fulltime     = $in['fulltime'];
                }
                $results->close();
            }
        }
    }
}

?>