<?php
/**
 *=-----------------------------------------------------------=
 * showday.php
 *=-----------------------------------------------------------=
 * Author: Marc Wandschneider:  2005-03-15
 *
 * This page shows the appointments for the current user
 * for the given day.  The day can be specified via GET
 * parameters:
 *
 * y = year
 * m = month
 * d = day.
 *
 * Or if no GET parameters are given, then the current date
 * is used.
 */
ob_start();
$page_title = "Show Appointments";

require_once('../libs/coreincs.inc');
require_once('../libs/pagetop.inc');


/**
 * First, see what date information we have.
 */
$year = isset($_GET['y']) ? $_GET['y'] : intval(date('Y'));
$month = isset($_GET['m']) ? $_GET['m'] : intval(date('m'));
$day = isset($_GET['d']) ? $_GET['d'] : intval(date('d'));
if (!checkdate($month, $day, $year))
{
  throw new InvalidDateException();
}

/**
 * Now get all the entries for this date.
 */
$start = new MyDateTime($year, $month, $day, 00, 00);
$end = new MyDateTime($year, $month, $day, 23, 59);

$am = AppointmentManager::getInstance();
$appts = $am->getAppointments($g_userID, $start, $end);

/**
 * Start the output
 */
$datestr = sprintf('%04d-%02d-%02d', $year, $month, $day);
$weekday = $start->getDayOfWeekString();
echo <<<EODISP
<h2 align='center'>Appointments for $datestr ($weekday)</h2>

EODISP;



if ($appts === NULL)
{
  echo <<<EOM
<p align='center'>
  You have no appointments scheduled for this day.
</p>

EOM;
}
else
{
  /**
   * List out the various entries in a nice XHTML table.
   */
  echo <<<EOT
<table align='center' width='80%' border='0' cellspacing='0'
       cellpadding='3' class='apptTable'>
<tr>
  <td width='25%' class='apptDispHeader'>When:</td>
  <td width='50%' class='apptDispHeader'>Title:</td>
  <td width='25%' class='apptDispHeader'>Where:</td>
</tr>

EOT;

  /**
   * Zip through all the appointments and print them out.
   */
  foreach ($appts as $appt)
  {
    if ($appt->StartTime->sameDay($appt->EndTime))
    {
      $start = $appt->StartTime->getTextTime();
      $end = $appt->EndTime->getTextTime();
    }
    else
    {
      $start = $appt->StartTime->getTextDate();
      $end = $appt->EndTime->getTextDate();
    }
    echo <<<EOAPPT
<tr>
  <td>$start - $end</td>
  <td>
    <a class='apptDispLink'
       href='showappt.php?aid={$appt->AppointmentID}'>
    {$appt->Title}
    </a>
  </td>
  <td>
    {$appt->Location}
  </td>
</tr>
EOAPPT;
  }

  /**
   * Close out the Table:
   */
  echo <<<EOT
</table>

EOT;
}

/**
 * Close and exit!
 */
require_once('../libs/appts/pagebottom.inc');
ob_end_flush();
?>
