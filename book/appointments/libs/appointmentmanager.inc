<?php
/**
 *=-----------------------------------------------------------=
 * appointmentmanager.inc
 *=-----------------------------------------------------------=
 * Author: Marc Wandschneider, 2005-03-15
 *
 * The AppointmentManager class is responsible for tracking
 * appointments in oursystem.  While the database is designed
 * with multiple users in mind, we are currently only going
 * to be giving it the same user all the time to keep the
 * sample simple.
 */
require_once('../libs/dbmanager.inc');
require_once('../libs/datetimehelpers.inc');


/**
 *=-----------------------------------------------------------=
 * Appointment
 *=-----------------------------------------------------------=
 * This is a simple class to hold the details for an
 * appointment, and saves us from the ugliness of simply
 * returning the fields from the database in a class.
 */
class Appointment
{
  public $AppointmentID;
  public $Title;
  public $StartTime;
  public $EndTime;
  public $Location;
  public $Description;

  public function __construct
  (
    $in_appt
  )
  {
    $this->AppointmentID = $in_appt['appt_id'];
    $this->Title = $in_appt['title'];
    $this->StartTime
        =  MyDateTime::fromDBString($in_appt['start_time']);
    $this->EndTime
        = MyDateTime::fromDBString($in_appt['end_time']);
    $this->Location = $in_appt['location'];
    $this->Description = $in_appt['description'];
  }
}



/**
 *=-----------------------------------------------------------=
 * AppointmentManager
 *=-----------------------------------------------------------=
 * This class is a single-instance class that manages
 * appointments in our database.  While the databases are
 * configured to permit multiple users, we have implemented
 * this sample for only one, keeping our code more
 * straightforward for now.
 */
class AppointmentManager
{
  /**
   * We only create one instance of this class, and this
   * contains that instance.
   */
  private static $s_apptManager;

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
   *    AppointmentManager
   */
  public static function getInstance()
  {
    if (AppointmentManager::$s_apptManager === NULL)
    {
      AppointmentManager::$s_apptManager
          = new AppointmentManager();
    }

    return AppointmentManager::$s_apptManager;
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
   *=---------------------------------------------------------=
   *=---------------------------------------------------------=
   *=---------------------------------------------------------=
   *                      Public Methods
   *=---------------------------------------------------------=
   *=---------------------------------------------------------=
   *=---------------------------------------------------------=
   *=---------------------------------------------------------=
   */

  /**
   *=---------------------------------------------------------=
   * addAppointment
   *=---------------------------------------------------------=
   * Adds the given appointment to the database.  Please note
   * that we do the necessary checking to make sure that there
   * are no appointments already scheduled for this time.
   *
   * Parameters:
   *    $in_userid    - userid of appt owner.
   *    $in_title     - title of meeting.
   *    $in_location  - where the meeting will take place.
   *    $in_start     - DateTime object for appt start.
   *    $in_end       - DateTime for appointment end time.
   *    $in_desc      - description of the meeting.
   *
   * Throws:
   *    AppointmentConflictException
   *    DatabaseErrorException
   */
  public function addAppointment
  (
    $in_userid,
    $in_title,
    $in_location,
    MyDateTime $in_start,
    MyDateTime $in_end,
    $in_desc
  )
  {
    /**
     * First, check to see if there are any appointments that
     * overlap this one.  Throw if there are.
     */
    if ($this->getAppointments($in_userid,
            $in_start, $in_end) != NULL)
      throw new AppointmentConflictException();

    /**
     * Get a connection.
     */
    $conn = DBManager::getConnection();

    /**
     * Get the data for insertion and make sure they're safe.
     * The htmlspecialchars() function helps us avoid both XSS
     * and SQL injection attacks (by replacing both HTML tags
     * and quotes)
     */
    $title = DBManager::mega_escape_string($in_title);
    $location = DBManager::mega_escape_string($in_location);
    $desc = DBManager::mega_escape_string($in_desc);
    $start = $in_start->dbString();
    $end = $in_end->dbString();

    /**
     * Build a query to insert the new appointment.
     */
    $query = <<<EOQUERY
INSERT INTO Appointments
  SET
    user_id = $in_userid,
    title = '$title',
    start_time = '$start',
    end_time = '$end',
    location = '$location',
    description = '$desc'
EOQUERY;

    /**
     * Execute the query!
     */
    $results = @$conn->query($query);
    if ($results === FALSE or $results === NULL)
      throw new DatabaseErrorException($conn->error);

    /**
     * We're done!
     */
  }


  /**
   *=---------------------------------------------------------=
   * getAppointments
   *=---------------------------------------------------------=
   * This method takes two parameters specifying a time
   * interval and returns a list of existing appointments
   * that occur during the given time interval.  If none
   * occur during that time period, then NULL is returned.
   *
   * Parameters:
   *    $in_userid      - userid of appointment managee
   *    $in_start       - start DateTime of interval
   *    $in_end         - end DateTime of interval
   *
   * Returns:
   *    Array of Appointment Objects.
   *
   * Throws:
   *    DatabaseErrorExeption
   */
  public function getAppointments
  (
    $in_userid,
    MyDateTime $in_start,
    MyDateTime $in_end
  )
  {
    /**
     * Get a database connection with which to work.
     */
    $conn = DBManager::getConnection();

    /**
     * Build a query to ask if there is any overlap.
     */
    $startstr = $in_start->dbString();
    $endstr = $in_end->dbString();
    $query = <<<EOQUERY
SELECT * FROM Appointments
  WHERE (start_time >= '$startstr' AND end_time <= '$endstr')
     OR ('$startstr' >= start_time AND '$startstr' <= end_time)
     OR ('$endstr' >= start_time AND '$endstr' <= end_time)
  ORDER BY start_time ASC
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
      $output [] = new Appointment($row);
    }

    /**
     * Clean up and return the matching appointments.
     */
    $results->close();
    return $output;
  }


  /**
   *=---------------------------------------------------------=
   * getPendingAppointments
   *=---------------------------------------------------------=
   * This method fetches the pending appointments for the
   * given userid, with the chronologically next one listed
   * first.  Only the first n are returned.
   *
   * Parameters:
   *    $in_userid          - fetch my appts
   *    $in_n               - [optional] fetch this many. 0
   *                          means fetch all of them.
   *
   * Returns:
   *    array of Appointment objects.
   *
   * Throws:
   *    DatabaseErrorException
   */
  public function getPendingAppointments($in_userid, $in_n = 0)
  {
    if ($in_n < 0)
      throw new InvalidArgumentException('$in_n');

    /**
     * Get a database connection with which to work.
     */
    $conn = DBManager::getConnection();

    /**
     * Build a query to get appointments.
     */
    $query = <<<EOQUERY
SELECT * FROM Appointments
  WHERE (start_time >= NOW())
  ORDER BY start_time ASC
EOQUERY;

    if ($in_n != 0)
    {
      $query .= " LIMIT 0, $in_n";
    }

    /**
     * Execute the query and look at the results.
     */
    $results = @$conn->query($query);
    if ($results === FALSE or $results === NULL)
      throw new DatabaseErrorException($conn->error);

    $output = NULL;
    while (($row = @$results->fetch_assoc()) != NULL)
    {
      $output [] = new Appointment($row);
    }

    /**
     * Clean up and return the matching appointments.
     */
    $results->close();
    return $output;
  }

  /**
   *=---------------------------------------------------------=
   * getAppointmentDetails
   *=---------------------------------------------------------=
   * Fetches an Appointment object for the given appointment
   * id (and userid).
   *
   * Parameters:
   *    $in_userid          - userid of requestor
   *    $in_apptid          - appointment desired.
   *
   * Returns:
   *    Appointment         - details.
   *
   * Throws:
   *    InvalidAppointmentException -- apptid is bogus or
   *            not owned by the given user.
   *    DatabaseErrorException
   *    InternalErrorException
   */
  public function getAppointmentDetails($in_userid, $in_apptid)
  {
    if (!is_int($in_apptid))
      throw new InvalidArgumentException('$in_apptid');

    /**
     * Get a database connection with which to work.
     */
    $conn = DBManager::getConnection();

    /**
     * Build a query to get the appointment.
     */
    $query = <<<EOQUERY
SELECT * FROM Appointments WHERE appt_id = $in_apptid
EOQUERY;

    $results = @$conn->query($query);
    if ($results === FALSE or $results === NULL)
      throw new DatabaseErrorException($conn->error);

    /**
     * Look at the results and make sure the userid matches.
     */
    if ($results->num_rows == 0)
    {
      $results->close();
      throw new InvalidAppointmentExeption();
    }
    else if ($results->num_rows != 1)
    {
      $results->close();
      throw new InternalErrorException('duplicate apptids!!');
    }
    else
    {
      /**
       * Otherwise, everything looks good.  Make sure the
       * userids match up and then return the Appointment
       * object.
       */
      $row = @$results->fetch_assoc();
      $results->close();
      if ($row['user_id'] != $in_userid)
      {
        throw new InvalidAppointmentException();
      }

      return new Appointment($row);
    }
  }

}


?>
