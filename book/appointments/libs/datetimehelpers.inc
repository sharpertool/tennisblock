<?php
/**
 *=-----------------------------------------------------------=
 * datetimehelpers.inc
 *=-----------------------------------------------------------=
 * Author: Marc Wandschneider, 2005-03-15
 *
 * This file contains a class that we will use to encapsulate
 * a Date and Time value.  The Time will only consist of hours
 * and minutes, so 0.00 will be the beginning of a day and
 * 23.59 will be the end of a day.
 */

/**
 * These values show how MySQL formats a DATETIME value when
 * returning data.  A field is "YYYY-MM-DD HH:MM"
 */
define('DB_DATETIMESEP', ' ');
define('DB_DATESEP', '-');
define('DB_TIMESEP', ':');
define('DB_FORMAT', '%1$d-%2$d-%3$d %4$d:%5$d');

/**
 * Important date lengths (in seconds)
 */
define('DAY_IN_SECS', 86400);
define('WEEK_IN_SECS', 604800);

/**
 *=-----------------------------------------------------------=
 * MyDateTime
 *=-----------------------------------------------------------=
 * This class contains a number of routines to help us process
 * dates and times in our web application.  The constructor
 * expects a date broken up into year, month, and day values,
 * as well as hour and minute time values.
 */
class MyDateTime
{
  /**
   * These are the public variables that people can query on
   * this object.  They should probably not be changed by
   * users.
   */
  public $Year;
  public $Month;
  public $Day;
  public $Hour;
  public $Minute;

  /**
   *=---------------------------------------------------------=
   * __construct
   *=---------------------------------------------------------=
   * Initialises a new instance of this class.  The parameters
   * are the values to actually be used for the date and time,
   * and none are optional.  All must be integers.
   *
   * Parameters:
   *    $in_year
   *    $in_month
   *    $in_day
   *    $in_hour
   *    $in_minute
   *
   * Throws:
   *    InvalidDateException
   *    InvalidTimeException
   */
  public function __construct
  (
    $in_year,
    $in_month,
    $in_day,
    $in_hour,
    $in_minute
  )
  {
    $this->Year = $in_year;
    $this->Month = $in_month;
    $this->Day = $in_day;
    $this->Hour = $in_hour;
    $this->Minute = $in_minute;

    /**
     * Make sure we are given a valid date and time!
     */
    if (!checkdate($in_month, $in_day, $in_year))
      throw new InvalidDateException();
    else if (!MyDateTime::validTime($in_hour, $in_minute))
      throw new InvalidTimeException();
  }

  /**
   *=---------------------------------------------------------=
   * fromDBString
   *=---------------------------------------------------------=
   * Given a string for a date and time that we received from
   * a database, go and return the equivalent MyDateTime object
   * for this value. This is a static method and is another
   * way of creating a MyDateTime object instead of simply using
   * the constructor.
   *
   * Parameters:
   *    $in_string          - string from the db field.
   *
   * Returns:
   *    MyDateTime            - datetime object representing that
   *                          string.
   */
  public static function fromDBString($in_string)
  {
    /**
     * Datetimes from DB are "date time".  split those apart
     * first.
     */
    $comps = explode(DB_DATETIMESEP, $in_string);

    /**
     * Now process date. YYYY-MM-DD
     */
    $dparts = explode(DB_DATESEP, $comps[0]);

    /**
     * and Time: HH:MM[:SS]
     */
    $tparts = explode(DB_TIMESEP, $comps[1]);

    /**
     * Create the MyDateTime object ...
     */
    return new MyDateTime($dparts[0], $dparts[1], $dparts[2],
                        $tparts[0], $tparts[1]);
  }

  /**
   *=---------------------------------------------------------=
   * validTime
   *=---------------------------------------------------------=
   * A static method that returns a Boolean indicating wheterh
   * the given hour and minutes form a valid time.
   *
   * Parameters:
   *    $in_hour
   *    $in_minutes
   *
   * Returns:
   *    Boolean - TRUE == valid, FALSE == invalid.
   */
  public static function validTime($in_hour, $in_minute)
  {
    if ($in_hour < 0 or $in_hour > 23
        or $in_minute < 0 or $in_minute > 59)
    {
      return FALSE;
    }
    else
    {
      return TRUE;
    }
  }




  /**
   *=---------------------------------------------------------=
   * sameDay
   *=---------------------------------------------------------=
   * Asks whether the given MyDateTime object represents the
   * same date as this one.  The time is completely ignored.
   *
   * Parameters:
   *    $in_dt2         - is this the same day as us?
   *
   * Returns:
   *    TRUE == yes, same, FALSE == nope, different dates.
   */
  public function sameDay(MyDateTime $in_dt2)
  {
    return ($in_dt2->Year == $this->Year
            and $in_dt2->Month == $this->Month
            and $in_dt2->Day == $this->Day) ? TRUE : FALSE;
  }


  /**
   *=---------------------------------------------------------=
   * greaterThan
   *=---------------------------------------------------------=
   * Checks to see if we are "greater than" the given MyDateTime
   * value.  We will use the timestamp functionality to
   * make this much easier.  The 1970-2038 restriction will not
   * prove fatal in any way for this application.
   *
   * Parameters:
   *    $in_dt2         - we are greater than this time?
   *
   * Returns:
   *    TRUE == we are greater, FALSE == $in_dt2 is greater.
   */
  public function greaterThan($in_dt2)
  {
    $ts1 = mktime($this->Hour, $this->Minute, 0, $this->Month,
                  $this->Day, $this->Year);
    $ts2 = mktime($in_dt2->Hour, $in_dt2->Minute, 0,
                  $in_dt2->Month, $in_dt2->Day, $in_dt2->Year);
    return ($ts1 > $ts2);
  }


  /**
   *=---------------------------------------------------------=
   * getDayOfWeekInt
   *=---------------------------------------------------------=
   * Returns the day of the week as an integer, with 0 being
   * sunday and 6 being saturday.
   *
   * Returns:
   *    Integer.
   *
   * Notes:
   *    We use timestamp functionality for this which limits
   *    us to 1970-2038.
   */
  public function getDayOfWeekInt()
  {
    $ts = mktime(0, 0, 0, $this->Month, $this->Day,
                 $this->Year);
    return intval(date('w', $ts));
  }



  /**
   *=---------------------------------------------------------=
   * getDayOfWeekString
   *=---------------------------------------------------------=
   * Returns the day of the week as an string
   *
   * Returns:
   *    string
   *
   * Notes:
   *    We use timestamp functionality for this which limits
   *    us to 1970-2038.
   */
  public function getDayOfWeekString()
  {
    $ts = mktime(0, 0, 0, $this->Month, $this->Day,
                 $this->Year);
    return date('l', $ts);
  }

  /**
   *=---------------------------------------------------------=
   * topOfWeek
   *=---------------------------------------------------------=
   * Returns a MyDateTime object which representes 00.00
   * (midnight) of the first day of the week in which the
   * current MyDateTime lies.
   *
   * Returns:
   *    MyDateTime   - beginning of first day of the current
   *                 week.
   *
   * Notes:
   *    We use timestamp functionality for this which limits
   *    us to 1970-2038.
   */
  public function topOfWeek()
  {
    /**
     * We're going to use the Unix Timestamp functions here,
     * and just stipulate that our system is not useful
     * for scheduling appointments prior to 1970 or after
     * 2038.  We can use the PEAR Date class if we want
     * maximal flexibility.
     */
    $ts = mktime(0, 0, 0, $this->Month, $this->Day,
                 $this->Year);

    /**
     * Find out what day of the week we are and then subtract
     * an appropriate number of seconds for each of those
     * days.
     */
    $dw = intval(date('w', $ts));
    $diff = DAY_IN_SECS * $dw;

    /**
     * With our new time, go and get the datetime values
     * for it.
     */
    $ts2 = $ts - $diff;
    $str = date('Y m d', $ts2);
    $parts = explode(' ', $str);
    return new MyDateTime(intval($parts[0]), intval($parts[1]),
                        intval($parts[2]), 0, 0);
  }

  /**
   *=---------------------------------------------------------=
   * bottomOfWeek
   *=---------------------------------------------------------=
   * Returns a MyDateTime object which representes 23.59
   * (11.59pm) of the last day of the week in which the
   * current MyDateTime lies.
   *
   * Returns:
   *    MyDateTime   - end of last day of the current
   *                 week.
   *
   * Notes:
   *    We use timestamp functionality for this which limits
   *    us to 1970-2038.
   */
  public function bottomOfWeek()
  {
    /**
     * We're going to use the Unix Timestamp functions here,
     * and just stipulate that our system is not useful
     * for scheduling appointments prior to 1970 or after
     * 2038.  We can use the PEAR Date class if we want
     * maximal flexibility.
     */
    $ts = mktime(0, 0, 0, $this->Month, $this->Day,
                 $this->Year);

    /**
     * Find out what day of the week we are and then subtract
     * an appropriate number of seconds for each of those
     * days.
     */
    $dw = intval(date('w', $ts));
    $diff = DAY_IN_SECS * (6 - $dw);

    /**
     * With our new time, go and get the datetime values
     * for it.
     */
    $ts2 = $ts + $diff;
    $str = date('Y m d', $ts2);
    $parts = explode(' ', $str);
    return new MyDateTime(intval($parts[0]), intval($parts[1]),
                        intval($parts[2]), 23, 59);
  }

  /**
   *=---------------------------------------------------------=
   * topOfMonth
   *=---------------------------------------------------------=
   * Returns a MyDateTime object which representes 00.00
   * (midnight) of the first day of the month in which the
   * current MyDateTime lies.
   *
   * Returns:
   *    MyDateTime   - beginning of first day of the current
   *                 month.
   */
  public function topOfMonth()
  {
    return new MyDateTime($this->Year, $this->Month, 1, 0, 0);
  }

  /**
   *=---------------------------------------------------------=
   * bottomOfMonth
   *=---------------------------------------------------------=
   * Returns a MyDateTime object which representes 23.59
   * (11.59pm) of the last day of the month in which the
   * current MyDateTime lies.
   *
   * Returns:
   *    MyDateTime   - end of last day of the current
   *                 month.
   */
  public function bottomOfMonth()
  {
    /**
     * This is a bit cheesy, but just go back from 31 until we
     * find a day that is valid in this month.  It WILL be
     * greater than 27.
     */
    for ($x = 31; $x > 27; $x--)
    {
      if (checkdate($this->Month, $x, $this->Year))
        break;
    }

    return new MyDateTime($this->Year, $this->Month, $x, 23, 59);
  }

  /**
   *=---------------------------------------------------------=
   * nextDay
   *=---------------------------------------------------------=
   * Returns a MyDateTime object for the day following this. Due
   * to all the possible nastiness that can occur with rolling
   * over into new months, years, leap years, etc., we use the
   * timestamp functions to do most of the hard work for us.
   *
   * Returns:
   *    MyDateTime with the next day.
   *
   * Notes:
   *    We use timestamp functionality for this which limits
   *    us to 1970-2038.
   */
  public function nextDay()
  {
    $ts = mktime(0, 0, 0, $this->Month, $this->Day,
                 $this->Year);
    $ts += DAY_IN_SECS;
    $str = date('Y m d', $ts);
    $parts = explode(' ', $str);
    return new MyDateTime(intval($parts[0]), intval($parts[1]),
                        intval($parts[2]), 23, 59);
  }

  /**
   *=---------------------------------------------------------=
   * containedInDates
   *=---------------------------------------------------------=
   * Asks whether the current MyDateTime is contained within the
   * interval specified by the two provided MyDateTime values.
   *
   * Parameters:
   *    $in_start           - start of test interval
   *    $in_end             - end of test interval
   *
   * Returns:
   *    Boolean, TRUE == we are contained, FALSE == not at all.
   *
   * Notes:
   *    We use timestamp functionality for this which limits
   *    us to 1970-2038.
   */
  public function containedInDates
  (
    MyDateTime $in_start,
    MyDateTime $in_end
  )
  {
    $s_ts = mktime(0, 0, 0, $in_start->Month, $in_start->Day,
                   $in_start->Year);
    $e_ts = mktime(23, 59, 59, $in_end->Month, $in_end->Day,
                   $in_end->Year);
    $ts = mktime(0, 0, 0, $this->Month, $this->Day,
                 $this->Year);
    if ($ts >= $s_ts and $ts <= $e_ts)
      return TRUE;
    else
      return FALSE;
  }


  /**
   *=---------------------------------------------------------=
   * addOneWeek
   *=---------------------------------------------------------=
   * Returns a new MyDateTime object that represents our current
   * value PLUS one week.
   *
   * Returns:
   *    A MyDateTime object for the same day of the week and time
   *    but NEXT week.
   *
   * Notes:
   *    We use timestamp functionality for this which limits
   *    us to 1970-2038.
   */
  public function addOneWeek()
  {
    $ts = mktime(0, 0, 0, $this->Month, $this->Day, $this->Year);
    $ts += WEEK_IN_SECS;
    if (!is_int($ts))
    {
      return new MyDateTime(2037, 12, 31, 23, 59);
    }

    $str = date('Y m d', $ts);
    $parts = explode(' ', $str);
    return new MyDateTime(intval($parts[0]), intval($parts[1]),
                        intval($parts[2]), 0, 0);
  }

  /**
   *=---------------------------------------------------------=
   * subOneWeek
   *=---------------------------------------------------------=
   * Returns a new MyDateTime object that represents our current
   * value SUBTRACT one week.
   *
   * Returns:
   *    A MyDateTime object for the same day of the week and time
   *    but LAST week.
   *
   * Notes:
   *    We use timestamp functionality for this which limits
   *    us to 1970-2038.
   */
  public function subOneWeek()
  {
    $ts = mktime(0, 0, 0, $this->Month, $this->Day, $this->Year);
    $ts -= WEEK_IN_SECS;
    if (!is_int($ts))
    {
      return new MyDateTime(1970, 1, 1, 0, 0);
    }

    $str = date('Y m d', $ts);
    $parts = explode(' ', $str);
    return new MyDateTime(intval($parts[0]), intval($parts[1]),
                        intval($parts[2]), 0, 0);
  }


  /**
   *=---------------------------------------------------------=
   * dbString
   *=---------------------------------------------------------=
   * Returns this date/time value in a format acceptable to
   * database.  We'll use a format string and sprintf to
   * provide maximal flexiblity in case we change DB engines.
   */
  public function dbString()
  {
    return sprintf(DB_FORMAT, $this->Year, $this->Month,
                   $this->Day, $this->Hour, $this->Minute);
  }

  /**
   *=---------------------------------------------------------=
   * getMonthDayText
   *=---------------------------------------------------------=
   * Returns a little string containing the short name of the
   * month and the day in that month.
   *
   * For example:   Aug-23
   *
   * Returns:
   *    string
   *
   * Notes:
   *    We use timestamp functionality for this which limits
   *    us to 1970-2038.
   */
  public function getMonthDayText()
  {
    $tm = mktime(0, 0, 0, $this->Month, $this->Day,
                 $this->Year);
    return date('M-d', $tm);
  }

  /**
   *=---------------------------------------------------------=
   * getTextTime
   *=---------------------------------------------------------=
   * Returns the time of this object as a string, optionally in
   * 24hr format.
   *
   * Parameters:
   *    $in_24hr        - [optional] use 24hr time instead of
   *                      12hr time?
   *
   * Returns:
   *    Time as a string:  "11:34AM", "23:55"
   */
  public function getTextTime($in_24hr = FALSE)
  {
    $hr = $this->Hour;
    $mn = $this->Minute;
    $ext = '';

    if ($in_24hr == FALSE)
    {
      if ($this->Hour > 12)
      {
        $hr -= 12;
        $ext = 'PM';
      }
      else
      {
        $ext = 'AM';
        if ($hr == 0)
        {
          $hr = 12;
        }
      }
    }

    return sprintf('%02d:%02d', $hr, $mn) . $ext;
  }

  /**
   *=---------------------------------------------------------=
   * getTextDate
   *=---------------------------------------------------------=
   * Returns the date as a string in the format YYYY-MM-DD
   *
   * Returns:
   *    string
   */
  public function getTextDate()
  {
    return sprintf('%04d-%02d-%02d', $this->Year, $this->Month,
                   $this->Day);
  }

  /**
   *=---------------------------------------------------------=
   * getTextDateTime
   *=---------------------------------------------------------=
   * Returns the date and the time as a string.
   *
   * Returns:
   *    string
   */
  public function getTextDateTime()
  {
    return $this->getTextDate() . ' ' . $this->getTextTime();
  }


  /**
   *=---------------------------------------------------------=
   * getMonthName
   *=---------------------------------------------------------=
   * Returns the name of the month.
   *
   * Returns:
   *    string.
   *
   * Notes:
   *    We use timestamp functionality for this which limits
   *    us to 1970-2038.
   */
  public function getMonthName()
  {
    $ts = mktime(0, 0, 0, $this->Month, $this->Day,
                 $this->Year);
    return date('F', $ts);
  }

}


?>
