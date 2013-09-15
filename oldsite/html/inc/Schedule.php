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
require_once('../inc/Player.php');
require_once('../inc/Season.php');
#require_once('../inc/datetimehelpers.php');

class Game
{
    public $court;
    public $teamA;
    public $teamB;
    
    public function __construct($incourt)
    {
        $this->court = $incout;
        $this->teamA = -1;
        $this->teamB = -1;
    }
}

/**
*=-----------------------------------------------------------=
* Set - consists of 3 games on 3 courts
*=-----------------------------------------------------------=
* This is a simple class to hold the details for an
* schedule
*/
class Set
{
    // 3 games in an array
    public $games;
    
    public function __construct()
    {
        $this->games[1] = new Game();
        $this->games[2] = new Game();
        $this->games[3] = new Game();
    }
}

/**
*=-----------------------------------------------------------=
* Match - contains a match, or 3 sets.
*=-----------------------------------------------------------=
* This is a simple class to hold the details for an
* schedule
*/
class Match
{
    public $MatchID;
    public $Date;
    public $Description;
    public $Players;
    public $Holdout;
    
    public function __construct($matchid,$date=NULL,$desc=NULL,$holdout=0)
    {
        $this->MatchID        = $matchid;
        $this->Date           = $date;
        $this->Description    = $desc;
        $this->Holdout        = $holdout;
    }
    
    public function setHoldout($bval)
    {
        $this->Holdout = $bval;
    }
    
    public function AddScheduledPlayer($row)
    {
        $this->Players[] = new Player($row);
    }
}



/**
*=-----------------------------------------------------------=
* ScheduleManager
*=-----------------------------------------------------------=
* This class is a single-instance class that manages
* appointments in our database.  While the databases are
* configured to permit multiple users, we have implemented
* this sample for only one, keeping our code more
* straightforward for now.
*/
class ScheduleManager
{
    /**
    * We only create one instance of this class, and this
    * contains that instance.
    */
    private static $s_schManager;
    private $matches;
    private $s_season;
    private $s_ncourts;
    private $s_sid;
    
    /**
    *=---------------------------------------------------------=
    * getInstance
    *=---------------------------------------------------------=
    * A static method that returns an instance of the
    * AppointmentManager object.  We only create one of these, so
    * we return the same instance on repeated calls to this
    * method.
    *
    * Returns:
    *    ScheduleManager
    */
    public static function getInstance()
    {
        if (ScheduleManager::$s_schManager === NULL)
        {
            ScheduleManager::$s_schManager = new ScheduleManager();
        }
    
        return ScheduleManager::$s_schManager;
    }
    
    /**
    *=---------------------------------------------------------=
    * __construct
    *=---------------------------------------------------------=
    * We don't want anybody to call this except for getInstance
    * above, so we made this routine private.
    */
    private function __construct()
    {
		/* Set the default season */
		ScheduleManager::$s_season = "2012 Fall";
		ScheduleManager::$s_ncourts= 3;
    }
    
    /**
    *=---------------------------------------------------------=
    * __destruct
    *=---------------------------------------------------------=
    * cleans up this instance.
    */
    function __destruct()
    {
    }
    
    public function setSeason($season)
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        $seasons = array();
        if ($results = @$conn->query("select sid,season,courts,firstcourt from seasons where season = '$season'")) {
            if ($results === FALSE or $results === NULL)
                throw new DatabaseErrorException($conn->error);
            
            while (($row = $results->fetch_assoc()) != NULL) {
                $seasons[] = new Season($row);
            }
            $results->close();
        }
        
        if (count($seasons)) {
            ScheduleManager::$s_season = $seasons[0]->season;
            ScheduleManager::$s_sid= $seasons[0]->sid;
            ScheduleManager::$s_ncourts = $seasons[0]->courts;
        }
    }
    
    public function getSeasons()
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        $seasons = array();
        if ($results = @$conn->query("select sid,season from seasons")) {
            if ($results === FALSE or $results === NULL)
                throw new DatabaseErrorException($conn->error);
            
            while (($row = $results->fetch_assoc()) != NULL) {
                $seasons[] = new Season($row);
            }
            $results->close();
        }
        
        return $seasons;
    }
    
    public function getCourtCount()
    {
        return ScheduleManager::$s_ncourts;
    }
    
    public function getFirstMatchDate()
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        $date = "";
        if ($results = @$conn->query("select date from blockmeetings where season = '$season' order by date")) {
            if ($results === FALSE or $results === NULL)
                throw new DatabaseErrorException($conn->error);
            
            if ($results->num_rows > 0) {
                $row = @$results->fetch_assoc();
                if ($row != NULL) {
                  $date = $row['date'];
                }
            }
            $results->close();
        }
        return $date;
    }
    
    public function getMatchid($date)
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        $d = date("Y-m-d",$date);
        
        $holdout = False;
        if ($results = @$conn->query("select meetid from blockmeetings where date = '$d' and season = '$season'")) {
            if ($results === FALSE or $results === NULL)
                throw new DatabaseErrorException($conn->error);
            
            $matchid = NULL;
            if ($results->num_rows == 1) {
                $row = @$results->fetch_assoc();
                if ($row != NULL) {
                    $matchid = $row['meetid'];
                }
            }
            $results->close();
        }
        return $matchid;
    }
    
    public function IsHoldout($date)
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        $season = ScheduleManager::$s_season;
        $d = date("Y-m-d",$date);
        
        $holdout = False;
        if ($results = @$conn->query("select holdout from blockmeetings where date = '$d' and season = '$season'")) {
            if ($results === FALSE or $results === NULL)
                throw new DatabaseErrorException($conn->error);
            
            if ($results->num_rows == 1) {
                $row = @$results->fetch_assoc();
                if ($row != NULL) {
                    if ($row['holdout'] == 1) {
                        $holdout = True;
                    }
                }
            }
            $results->close();
        }
        
        return $holdout;
    }
    
    public function LastBlockDate()
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        $season = ScheduleManager::$s_season;
        
        if ($results = @$conn->query("select max(date) mdate from blockmeetings where season = '$season'")) {
            if ($results === FALSE or $results === NULL)
                throw new DatabaseErrorException($conn->error);
            
            if ($results->num_rows == 1) {
                $row = @$results->fetch_assoc();
                if ($row != NULL) {
                    $date = $row['mdate'];
                }
            }
            $results->close();
        }
        
        return $date;
    }

    /**
    *=---------------------------------------------------------=
    * getMatchByID
    *=---------------------------------------------------------=
    * This method takes two parameters specifying a time
    * interval and returns a list of existing appointments
    * that occur during the given time interval.  If none
    * occur during that time period, then NULL is returned.
    *
    * Parameters:
    *    $in_matchid      - userid of appointment managee
    *
    * Returns:
    *    A single Match object
    *
    * Throws:
    *    DatabaseErrorExeption
    */
    public function getMatchByID  ($in_matchid)
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        /**
        * Build a query to ask if there is any overlap.
        */
        $query = <<<EOQUERY
        SELECT
        firstname,
        lastname,
        gender,
        NTRP,
        microNTRP,
        email,
        home,
        cell,
        work,
        date,
        comments,
        sub
        from
        blockmeetings bm, schedule s, players p
        where 
        bm.meetid = s.matchid
        and s.pid = p.pid
        and bm.meetid = $in_matchid
        and bm.season = '$season'
        order by
        gender,p.pid
        ;
EOQUERY;
    
    
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL)
            throw new DatabaseErrorException($conn->error);
        
        $output = NULL;
        $match = new Match($in_matchid);
        while (($row = @$results->fetch_assoc()) != NULL) 
        {
            $match->AddScheduledPlayer($row);
        }
        
        /**
        * Clean up and return the matching appointments.
        */
        $results->close();
        return $match;
    }
    
    /**
    *=---------------------------------------------------------=
    * GetNextGroup
    *=---------------------------------------------------------=
    */
    public function getNextGroup($timestamp) 
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        $season = ScheduleManager::$s_season;
        $d = date("Y-m-d",$timestamp);
        
        // Get a list of full-time couples.
        // Add these to the "scheduled" list first
        
        // Need to select these by date.. due to availability
        $query = <<<EOQUERY
        select *
        from couples
        where
        fulltime = 1
        and pa_id not in (select pid from availability where date = '$d' and unavailable=1)
        and pb_id not in (select pid from availability where date = '$d' and unavailable=1)
        and blockcouple = 1
        and season = "$season"
EOQUERY;
        
        $couples = array();
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL) {
            $needed = ScheduleManager::$s_ncourts*2 - count($couples);
        } else {
            while (($row = $results->fetch_assoc()) != NULL) {
                $couples[] = new Couple($row);
            }
            $needed = ScheduleManager::$s_ncourts*2 - count($couples);
            
        }
            
        
        // Fill in with couples that have not played yet.
        // I need to check if there are any records scheduled first,
        // if not, then do a diferent query
        $query = "select * from schedule";
        $results = @$conn->query($query);
        if ($results->num_rows > 0) {
            // Use my query when there are some couples scheduled already
            $query = <<<EOQUERY
            select distinct coupleid
            from couples,schedule,availability,blockmeetings 
            where
            couples.season = '$season'
            and fulltime = 0
            and pa_id not in (select pid from schedule where season = '$season')
            and pb_id not in (select pid from schedule where season = '$season')
            and pa_id not in (select pid from availability where date = '$d' and unavailable=1 and season = '$season')
            and pb_id not in (select pid from availability where date = '$d' and unavailable=1 and season = '$season')
            and blockcouple = 1
            and couples.season = "$season"
            ;
EOQUERY;
        } else {
            // Use this query where there is nothing scheduled at all.
            $query = <<<EOQUERY
            select distinct coupleid
            from couples
            where
            fulltime = 0
            and pa_id not in (select pid from availability where date = '$d' and unavailable=1)
            and pb_id not in (select pid from availability where date = '$d' and unavailable=1)
            and blockcouple = 1
            and season = '$season'
            ;
EOQUERY;
        }
        
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL)
            throw new DatabaseErrorException($conn->error);
        
        $temp_couples=array();
        while (($row = $results->fetch_assoc()) != NULL) {
            $temp_couples[] = new Couple($row['coupleid']);
        }
        $results->close();
        srand((float)microtime() * 1000000);
        shuffle($temp_couples);
        
        // Now, take couples from this list in random order
        // until we run out of $temp_couples or we get 6 total
        // PHP has a nice function for this.
        if (count($temp_couples) >= $needed) {
            $couples = array_merge($couples,array_slice($temp_couples,0,$needed));
        } else {
            // Take all of these
            $couples = array_merge($couples,$temp_couples);
        }
        
        $needed = ScheduleManager::$s_ncourts*2 - count($couples);
        
        if ($needed == 0) {
            return $couples;
        }
        
        // Do we still need more?? If so, then find the couples with the 
        // least number of plays.
        $query = <<<EOQUERY
        select count(coupleid) nplays,coupleid,meetid,date
        from couples,schedule,blockmeetings 
        where
        blockmeetings.season = '$season'
        and fulltime = 0
        and schedule.matchid = blockmeetings.meetid 
        and (pa_id = pid or pb_id = pid)
        and pa_id not in (select pid from availability where date = '$d' and unavailable=1)
        and pb_id not in (select pid from availability where date = '$d' and unavailable=1)
        and blockcouple = 1
        and couples.season = "$season"
        group by coupleid
        order by nplays asc
        ;
EOQUERY;
        
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL)
            throw new DatabaseErrorException($conn->error);
        
        $temp_couples = array();
        while (($row = @$results->fetch_assoc()) != NULL) 
        {
            $c = new Couple($row['coupleid']);
            $c->nplays = $row['nplays'];
            $temp_couples[] = $c;
        }
        $results->close();
        #shuffle($temp_couples);
        
        // Keep iterating, finding those with the fewest plays first.
        $nplays = $temp_couples[0]->nplays;
        $temp = array();
        foreach ($temp_couples as $couple) {
            if ($couple->nplays == $nplays) {
                $temp[] = $couple;
            } else {
            // the nPlays has changed, take the coules we have so far
            // and add them to the list.
            
            if (count($temp) >= $needed) {
                shuffle($temp);
                $couples = array_merge($couples,array_slice($temp,0,$needed));
                break;
            } else {
                // Take all of these
                $couples = array_merge($couples,$temp);
            }
            $needed = ScheduleManager::$s_ncourts*2 - count($couples);
            $temp = array();
            $nplays = $couple->nplays;
            $temp[] = $couple;
            if ($needed == 0 )
                break;
            }
        }
        
        $needed = ScheduleManager::$s_ncourts*2 - count($couples);
        if ($needed) {
            shuffle($temp);
            $couples = array_merge($couples,array_slice($temp,0,$needed));
        }
        
        return $couples;
    }
    
    public function clearSlotsByID($matchid) 
    {
        $conn = DBManager::getConnection();
        
        // Determine which dates have not been scheduled yet.
        // 
        $query = "delete from slots where matchid = $matchid";
        
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);
    }
    
    public function clearScheduleByID($matchid) {
        $conn = DBManager::getConnection();
        
        // Determine which dates have not been scheduled yet.
        // 
        $query = "delete from schedule where matchid = $matchid";
        
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);
    }
    
    /**
    *=---------------------------------------------------------=
    * ScheduleNextDate
    *=---------------------------------------------------------=
    */
    public function GetUnsheduledMathces() {
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        // Determine which dates have not been scheduled yet.
        // 
        $query = <<<EOQUERY
        select
        meetid,
        date
        from blockmeetings
        where
        season = '$season'
        and meetid not in ( select distinct matchid from schedule)
        and holdout = 0
        order by date
EOQUERY;
        
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL)
            throw new DatabaseErrorException($conn->error);
        
        while (($row = $results->fetch_assoc()) != NULL) {
            $matches[] = new Match($row['meetid'],$row['date']);
        }
        
        $results->close();
        return $matches;
    }
    
    public function AddCouplesToSchedule($matchid,$couples)
    {
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        foreach ($couples as $couple) {
            $id = $couple->paid;
            // Determine which dates have not been scheduled yet.
            // 
            $query = <<<EOQUERY
            insert into schedule
            (matchid,pid,sub,season)
            values ($matchid,$id,0,"$season")
EOQUERY;
            
            /**
            * Execute the query and look at the results.
            */
            $results = @$conn->query($query);
            if ($results === FALSE or $results === NULL)
                throw new DatabaseErrorException($conn->error);
            
            $id = $couple->pbid;
            // Determine which dates have not been scheduled yet.
            // 
            $query = <<<EOQUERY
            insert into schedule
            (matchid,pid,sub,season)
            values ($matchid,$id,0,"$season")
EOQUERY;
            
            /**
            * Execute the query and look at the results.
            */
            $results = @$conn->query($query);
            if ($results === FALSE or $results === NULL)
                throw new DatabaseErrorException($conn->error);
            
        }
    }
    
    public function GetPlayers() {
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        // Determine which dates have not been scheduled yet.
        // 
        $query = <<<EOQUERY
        select
        p.pid,
        coupleid,
        firstname,
        lastname,
        gender,
        NTRP,
        microNTRP,
        email,
        home,
        work,
        cell
        
        from players p,season_players sp,couples c
        where
        sp.season = '$season'
        and c.season = '$season'
        and p.pid = sp.pid
        and (p.pid = c.pa_id or p.pid = c.pb_id)
        and sp.blockmember = 1
        and c.blockcouple = 1
        
        order by coupleid, gender desc
EOQUERY;
        
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL)
            throw new DatabaseErrorException($conn->error);
        
        $players = array();
        while (($row = $results->fetch_assoc()) != NULL) {
            $players[] = new Player($row);
        }
        
        $results->close();
        return $players;
    }
    
    public function GetAllPlayers($timestamp) {
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        $sdate = date("Y-m-d",$timestamp);

        // Determine which dates have not been scheduled yet.
        // 
        $query = <<<EOQUERY
        select
        sp.pid,
        firstname,
        lastname,
        gender,
        NTRP,
        microNTRP,
        email,
        home,
        work,
        cell
        
        from
            season_players sp,
            players p
            
        where
            sp.season = '$season'
            and sp.pid = p.pid
            and sp.pid not in
                (select PID from availability
                    where
                        season = "$season"
                        and date = "$sdate"
                )
EOQUERY;
        
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL)
            throw new DatabaseErrorException($conn->error);
        
        $players = array();
        while (($row = $results->fetch_assoc()) != NULL) {
            $players[] = new Player($row);
        }
        
        $results->close();
        return $players;
    }
    
    public function GetPlayersByDate($ts) {
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        // Determine which dates have not been scheduled yet.
        //
        
        $sdate = date("Y-m-d",$ts);
        $query = <<<EOQUERY
        select
        meetid,
        firstname,
        lastname,
        gender,
        p.pid pid,
        s.schedid schedid,
        NTRP,
        microNTRP,
        email
        
        from blockmeetings bm,schedule s,players p
        where
        bm.season = '$season'
        and bm.date = "$sdate"
        and bm.meetid = s.matchid
        and s.pid = p.pid
        
EOQUERY;
        
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL) {
            throw new DatabaseErrorException($conn->error);
        }
        
        $matchid = NULL;
        $players = array();
        while (($row = $results->fetch_assoc()) != NULL) {
            $players[] = new Player($row);
            $matchid = $row['meetid'];
        }
        $results->close();
        
        return array($matchid,$players);
    }
    
    public function GetMatchPlayers($matchid) {

        $conn = DBManager::getConnection();
        
        // Determine which dates have not been scheduled yet.
        //
        
        $query = <<<EOQUERY
        select
            setnum, court, pid, position
        from
            slots s
        where
            s.matchid = $matchid
        order by setnum, court
        
EOQUERY;
        
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL) {
            throw new DatabaseErrorException($conn->error);
        }

        $sets[1] = array();
        $sets[2] = array();
        $sets[3] = array();
        $court = -1;
        while (($row = $results->fetch_assoc()) != NULL) {
            $courtdb = $row['court'];
            $setnum = $row['setnum'];
            if ($courtdb != $court) {
                $court = $courtdb;
            }
            $pos = $row['position'];
            $pid = $row['pid'];
            
            $sets[$setnum][$court][$pos] = Player::getPlayer($pid);
        }
        $results->close();
        
        return $sets;
    }
    
    public function UpdateSchedule($schedid,$pid) {
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        // Determine which dates have not been scheduled yet.
        // 
        $query = <<<EOQUERY
        update schedule
        set pid = $pid
        where schedid = $schedid
        ;
EOQUERY;
        
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL)
            throw new DatabaseErrorException($conn->error);
    }
        
    public function SetUnavailable($pid,$date) {
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        // Determine which dates have not been scheduled yet.
        // 
        $query = <<<EOQUERY
        insert into availability
        (pid,date,unavailable,reason,season)
        values
        ($pid,"$date",1,"","$season")
EOQUERY;
        
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL)
            throw new DatabaseErrorException($conn->error);
    }
        
    public function GetPlayersCountByID($playerid,$currdate) {
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        // Determine which dates have not been scheduled yet.
        //
        
        $query = <<<EOQUERY
        select
        count(*) numplays
        
        from blockmeetings bm,schedule s
        where
        bm.season = '$season'
        and bm.meetid = s.matchid
        and s.pid = $playerid
        and bm.date < '$currdate'
        
EOQUERY;
        
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL) {
            throw new DatabaseErrorException($conn->error);
        }
        
        if ($results->num_rows == 1) {
            $row = @$results->fetch_assoc();
            if ($row != NULL) {
                $count = $row['numplays'];
            }
        }
        $results->close();
        return $count;
    
    }
    
    public function SetAllAvailable() {
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        // Determine which dates have not been scheduled yet.
        // 
        $query = <<<EOQUERY
        delete from availability
        where season = '$season'
EOQUERY;
        
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results === FALSE)
            throw new DatabaseErrorException($conn->error);
    }
    
    public function GetMatchCount($currdate) {
        $conn = DBManager::getConnection();
        $season = ScheduleManager::$s_season;
        
        // Determine which dates have not been scheduled yet.
        //
        
        $query = <<<EOQUERY
        select
        count(distinct bm.meetid) numplays
        
        from
        blockmeetings bm, schedule s
        where
        bm.season = '$season'
        and bm.meetid = s.matchid
        and bm.date < '$currdate'
        
EOQUERY;
        
        /**
        * Execute the query and look at the results.
        */
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL) {
            throw new DatabaseErrorException($conn->error);
        }
        
        if ($results->num_rows == 1) {
            $row = @$results->fetch_assoc();
            if ($row != NULL) {
                $count = $row['numplays'];
            }
        }
        $results->close();
        return $count;
    
    }
}

?>
