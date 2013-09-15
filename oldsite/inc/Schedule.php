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
require_once('../inc/errors.inc');
#require_once('../inc/datetimehelpers.php');

class Game
{
    public $court;
    public $teamA;
    public $teamB;
    
    public function __construct($incourt)
    {
        $this->court = $incourt;
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
        $this->games[1] = new Game(1);
        $this->games[2] = new Game(2);
        $this->games[3] = new Game(3);
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
		$this->s_season = "2013 Fall";
		$this->s_sid = 1;
		$this->s_ncourts= 3;

		if (isset($_SESSION['season'])) {
			$this->setSeason($_SESSION['season']);
		} else {
			$this->setSeason("2013 Fall");
		}
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
		$season = "2013 Fall";
        
        $seasons = array();
        if ($results = @$conn->query("select id,name,courts,firstcourt from blockdb_season where name = '$season'")) {
            if ($results === FALSE or $results === NULL)
                throw new DatabaseErrorException($conn->error);
            
            while (($row = $results->fetch_assoc()) != NULL) {
                $seasons[] = new Season($row);
            }
            $results->close();
        }
        
        if (count($seasons)) {
            $this->s_season = $seasons[0]->season;
            $this->s_sid= $seasons[0]->sid;
            $this->s_ncourts = $seasons[0]->courts;
        }
    }

	public function getSeasonText() {
		if (isset($_SESSION['season'])) {
			$season = $_SESSION['season'];
		} else {
			$season = "2013 Fall";
		}
		if ($season == "2013 Fall") {
			$season_text =  "Fall, 2013 ";
		} else {
			$season_text = $season;
		}
		return $season_text;
	}
    
    public function getSeasons()
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        $seasons = array();
        if ($results = @$conn->query("select id,name,courts,firstcourt from blockdb_season")) {
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
        return $this->s_ncourts;
    }
    
    public function getFirstMatchDate()
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        $sid = $this->s_sid;
        
        $date = "";
        if ($results = @$conn->query("select date from blockdb_meetings where season_id = $sid order by date")) {
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
        $sid = $this->s_sid;
        
        $d = date("Y-m-d",$date);
        
        $holdout = False;
        if ($results = @$conn->query("select id from blockdb_meetings where date = '$d' and season_id = $sid")) {
            if ($results === FALSE or $results === NULL)
                throw new DatabaseErrorException($conn->error);
            
            $matchid = NULL;
            if ($results->num_rows == 1) {
                $row = @$results->fetch_assoc();
                if ($row != NULL) {
                    $matchid = $row['id'];
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

		$sid = $this->s_sid;
        $d = date("Y-m-d",$date);
        
        $holdout = False;
        if ($results = @$conn->query("select holdout from blockdb_meetings where date = '$d' and season_id = $sid")) {
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

		$sid = $this->s_sid;
        
        if ($results = @$conn->query("select max(date) mdate from blockdb_meetings where season_id = $sid")) {
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
		$sid = $this->s_sid;

        /**
        * Build a query to ask if there is any overlap.
        */
        $query = <<<EOQUERY
        SELECT
			first,
			last,
			gender,
			ntrp,
			microntrp,
			email,
			phone
        from
	        blockdb_meetings bm, blockdb_schedule s, blockdb_player p
        where 
			bm.id = s.meeting_id
			and s.pid_id = p.id
			and bm.id = $in_matchid
			and bm.season_id = $sid
		order by
			gender,p.id
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

		$sid = $this->s_sid;
        $d = date("Y-m-d",$timestamp);
        
        // Get a list of full-time couples.
        // Add these to the "scheduled" list first
        
        // Need to select these by date.. due to availability
        $query = <<<EOQUERY
        select *
        	from blockdb_couple
        where
        	fulltime = 1
			and male_id not in (select
                	player_id
                from
                	blockdb_availability av, blockdb_meetings mtg
                    where
                    	mtg.date = "$d"
                    	and mtg.season_id = $sid
                    	and av.meeting_id = mtg.id
                    	and av.available = 0
                )
			and female_id not in (select
                	player_id
                from
                	blockdb_availability av, blockdb_meetings mtg
                    where
                    	mtg.date = "$d"
                    	and mtg.season_id = $sid
                    	and av.meeting_id = mtg.id
                    	and av.available = 0
                )
			and blockcouple = 1
			and season_id = $sid
EOQUERY;
        
        $couples = array();
        $results = @$conn->query($query);
        if ($results === FALSE or $results === NULL) {
            $needed = $this->s_ncourts*2 - count($couples);
        } else {
            while (($row = $results->fetch_assoc()) != NULL) {
                $couples[] = new Couple($row);
            }
            $needed = $this->s_ncourts*2 - count($couples);
            
        }
            
        
        // Fill in with couples that have not played yet.
        // I need to check if there are any records scheduled first,
        // if not, then do a diferent query
        $query = "select * from blockdb_schedule";
        $results = @$conn->query($query);
        if ($results->num_rows > 0) {
            // Use my query when there are some couples scheduled already
            $query = <<<EOQUERY
            select
            	distinct coupleid
            from
            	blockdb_couple,schedule,availability,blockdb_meetings
            where
				blockdb_couple.season_id = $sid
				and fulltime = 0
				and pa_id not in (select pid from schedule where season_id = $sid)
				and pb_id not in (select pid from schedule where season_id = $sid)
				and pa_id not in (select pid from availability where date = '$d' and unavailable=1 and season_id = $sid)
				and pb_id not in (select pid from availability where date = '$d' and unavailable=1 and season_id = $sid)
				and blockcouple = 1
				and blockdb_couple.season_id = $sid
            ;
EOQUERY;
        } else {
            // Use this query where there is nothing scheduled at all.
            $query = <<<EOQUERY
            select
            	distinct coupleid
            from
            	blockdb_couple
            where
				fulltime = 0
				and pa_id not in (select pid from availability where date = '$d' and unavailable=1)
				and pb_id not in (select pid from availability where date = '$d' and unavailable=1)
				and blockcouple = 1
				and season_id = $sid
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
        select
        	count(coupleid) nplays,coupleid,meetid,date
        from
        	blockdb_couple,schedule,blockdb_meetings
        where
			blockdb_meetings.season = '$season'
			and fulltime = 0
			and schedule.matchid = blockdb_meetings.meetid
			and (pa_id = pid or pb_id = pid)
			and pa_id not in (select pid from availability where date = '$d' and unavailable=1)
			and pb_id not in (select pid from availability where date = '$d' and unavailable=1)
			and blockcouple = 1
			and blockdb_couple.season = "$season"
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
        $query = "delete from blockdb_slots where meeting_id = $matchid";
        
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
        $query = "delete from blockdb_schedule where meeting_id = $matchid";
        
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
		$sid = $this->s_sid;

        // Determine which dates have not been scheduled yet.
        // 
        $query = <<<EOQUERY
        select
			id,
			date
        from
        	blockdb_meetings
        where
			season_id = $sid
			and id not in ( select distinct meeting_id from blockdb_schedule)
			and holdout = 0
		order by
			date
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
		$sid = $this->s_sid;

        foreach ($couples as $couple) {
            $id = $couple->paid;
            // Determine which dates have not been scheduled yet.
            // 
            $query = <<<EOQUERY
            insert into
            	blockdb_schedule

            (meeting_id,pid_id,issub,season_id)
            values
            	($matchid,$id,0,$sid)
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
            (meeting_id,pid_id,sub,season_id)
            values ($matchid,$id,0,$sid)
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
        $season = $this->s_season;
        
        // Determine which dates have not been scheduled yet.
        // 
        $query = <<<EOQUERY
        select
        p.id,
        c.id as coupleid,
        first,
        last,
        gender,
        ntrp,
        microntrp,
        email,
        phone

        from blokdb_player p,blockdb_seasonplayers sp,blockdb_couple c
        where
        	sp.season_id = $sid
        and c.season_id = $sid
        and p.id = sp.player_id
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
		$sid = $this->s_sid;

        $sdate = date("Y-m-d",$timestamp);

        // Determine which dates have not been scheduled yet.
        // 
        $query = <<<EOQUERY
        select
			p.id,
			first,
			last,
			gender,
			ntrp,
			microntrp,
			email,
			phone

        from
            blockdb_seasonplayers sp,
            blockdb_player p
            
        where
            sp.season_id = $sid
            and sp.player_id= p.id
            and sp.player_id not in
                (select
                	player_id
                from
                	blockdb_availability av, blockdb_meetings mtg
                    where
                    	mtg.date = "$sdate"
                    	and mtg.season_id = $sid
                    	and av.meeting_id = mtg.id
                    	and av.available = 0
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
		$sid = $this->s_sid;

        // Determine which dates have not been scheduled yet.
        //
        
        $sdate = date("Y-m-d",$ts);
        $query = <<<EOQUERY
        select
			bm.id,
			first,
			last,
			gender,
			p.id pid,
			s.id schedid,
			ntrp,
			microntrp,
			email
        
        from blockdb_meetings bm,blockdb_schedule s,blockdb_player p
        where
			bm.season_id = $sid
			and bm.date = "$sdate"
			and s.meeting_id = bm.id
			and s.pid_id = p.id
        
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
        $season = $this->s_season;
        
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
        $season = $this->s_season;
        
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
        $season = $this->s_season;
        
        // Determine which dates have not been scheduled yet.
        //
        
        $query = <<<EOQUERY
        select
        count(*) numplays
        
        from blockdb_meetings bm,schedule s
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
        $season = $this->s_season;
        
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
        $season = $this->s_season;
        
        // Determine which dates have not been scheduled yet.
        //
        
        $query = <<<EOQUERY
        select
        count(distinct bm.meetid) numplays
        
        from
        blockdb_meetings bm, schedule s
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
