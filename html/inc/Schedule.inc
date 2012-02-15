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
require_once('../inc/dbmanager.inc');
#require_once('../inc/datetimehelpers.inc');

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

class Player
{
    public $firstname;
    public $lastname;
    public $NTRP;
    public $uNTRP;
    public $gender;

    public function __construct($dbrow = null)
    {
        if ($dbrow != NULL) {
            $firstname  = $dbrow['firstname'];
            $lastname   = $dbrow['lastname'];
            $NTRP       = $dbrow['NTRP'];
            $uNTRP      = $dbrow['microNTRP'];
            $gender     = $dbrow['gender'];
        }
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

  public function __construct
  (
    &$results
  )
  {
    // Each row contains:
      // schedid, matchid, pid, are they a sub?
    while (($row = @$results->fetch_assoc()) != NULL)
    {
      $output [] = new Appointment($row);
    }

    $this->AppointmentID = $in_appt['appt_id'];
    $this->Title = $in_appt['title'];
    $this->StartTime
        =  MyDateTime::fromDBString($in_appt['start_time']);
    $this->EndTime
        = MyDateTime::fromDBString($in_appt['end_time']);
    $this->Location = $in_appt['location'];
    $this->Description = $in_appt['description'];
  }
  
  public function AddScheduledPlayer($row)
  {
      $players[] = new Player($row);
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
      ScheduleManager::$s_schManager
          = new ScheduleManager();
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
  public function getMatchByID
  (
    $in_matchid
  )
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
    firstname,
    lastame,
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
    bm.matchid = s.matchid
    and s.pid = p.pid
    and bm.matchid = $in_matchid
order by
    gender,p.pid
EOQUERY;


    /**
     * Execute the query and look at the results.
     */
    $results = @$conn->query($query);
    if ($results === FALSE or $results === NULL)
      return null;
      throw new DatabaseErrorException($conn->error);

    $output = NULL;
    $match = new Match();
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

}


?>
