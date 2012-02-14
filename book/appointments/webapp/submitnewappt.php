<?php
/**
 *=-----------------------------------------------------------=
 * submitnewappt.php
 *=-----------------------------------------------------------=
 * Author: Marc Wandschneider:  2005-03-15
 *
 * The user has entered the information for a new
 * appointment.  Go and verify this information now, and
 * then confirm that there are no appointments in this time
 * frame.
 *
 * There is one concurrency risk in this application, but
 * only if we expand it to allow multiple users who can
 * schedule each other -- somebody could theoretically
 * create an appointment for us between our check to see
 * if we have an appointment and our insertion of an
 * appointment at a given time.  To solve this problem, we
 * would want to make sure that only one client program
 * (browser) was active for any one user at a given time.
 *
 * However, since this sample will initially be single user
 * only, we will not worry about this, and demonstrate
 * solutions to similar problems in the other samples.
 *
 */
ob_start();
$page_title = "Create New Appointment";

require_once('../libs/coreincs.inc');


/**
 *=-----------------------------------------------------------=
 * input_error_abort
 *=-----------------------------------------------------------=
 * If there is an input error, this function goes and saves
 * whatever input we have thus far in the session (so we can
 * put it back in the form) and sends the user back to the
 * addnewappt.php page to correct the error.
 *
 * Parameters:
 *      $in_code        - the error code to send back to
 *                        the addnewappt.php page.
 */
function input_error_abort($in_code)
{
  global $title, $location, $syear, $smonth, $sday, $stime,
         $eyear, $emonth, $eday, $etime, $desc;

  $_SESSION['apptinfo'] = array();
  $ai = &$_SESSION['apptinfo'];
  $ai['title'] = $title;
  $ai['location'] = $location;
  $ai['syear'] = $syear;
  $ai['smonth'] = $smonth;
  $ai['sday'] = $sday;
  $ai['stime'] = $stime;
  $ai['eyear'] = $eyear;
  $ai['emonth'] = $emonth;
  $ai['eday'] = $eday;
  $ai['etime'] = $etime;
  $ai['desc'] = $desc;

  header("Location: addnewappt.php?err=$in_code");
  ob_end_clean();
  exit;
}


/**
 * Determine what information we have so far.
 */
$title = isset($_POST['title']) ? $_POST['title'] : '';
$location = isset($_POST['location']) ? $_POST['location'] : '';
$syear = isset($_POST['syear']) ? $_POST['syear'] : '';
$smonth = isset($_POST['smonth']) ? $_POST['smonth'] : '';
$sday = isset($_POST['sday']) ? $_POST['sday'] : '';
$stime = isset($_POST['stime']) ? $_POST['stime'] : '';
$eyear = isset($_POST['eyear']) ? $_POST['eyear'] : '';
$emonth = isset($_POST['emonth']) ? $_POST['emonth'] : '';
$eday = isset($_POST['eday']) ? $_POST['eday'] : '';
$etime = isset($_POST['etime']) ? $_POST['etime'] : '';
$desc = isset($_POST['desc']) ? $_POST['desc'] : '';

echo "We have some info\n";
/**
 * Make sure we have valid parameters.  They must specify:
 *
 * - a title
 * - a valid start datetime
 * - a valid end datetime
 * - an end datetime that is greater than the start datetime.
 */
if ($title == '')
{
  input_error_abort('title');
}

/**
 * Start Date. Redirect back on error.
 */
try
{
  $time = explode('.', $stime);
  $start_date = new MyDateTime($syear, $smonth, $sday,
                             $time[0], $time[1]);
}
catch (InvalidDateException $ide)
{
  input_error_abort('sdate');
}
catch (InvalidTimeException $ite)
{
  input_error_abort('stime');
}

/**
 * End Date.  Redirect back on error.
 */
try
{
  $time = explode('.', $etime);
  $end_date = new MyDateTime($eyear, $emonth, $eday,
                           $time[0], $time[1]);
}
catch (InvalidDateException $ide)
{
  input_error_abort('edate');
}
catch (InvalidTimeException $ite)
{
  input_error_abort('etime');
}

/**
 * End DateTime > start DateTime
 */
if (!$end_date->greaterThan($start_date))
{
  input_error_abort('lesser');
}

/**
 * Okay, input values verified.   Get an AppointmentManager
 * and ask it to add the appointment.  If there are any
 * conflicts, it will throw an AppointmentConflictException,
 * which we can trap and use to redirect the user back to the
 * addnewappt.php page ...
 */
$am = AppointmentManager::getInstance();
try
{
  $am->addAppointment($g_userID, $title, $location,
                      $start_date, $end_date, $desc);
}
catch (AppointmentConflictException $ace)
{
  input_error_abort('conflict');
}

/**
 * Success!  Clean up and redirect the user to the appropriate
 * date to show their appointments on that date.
 */
if (isset($_SESSION['apptinfo']))
{
  unset($_SESSION['apptinfo']);
}
header("Location: showday.php?y=$syear&m=$smonth&d=$sday");
ob_end_clean();
?>
