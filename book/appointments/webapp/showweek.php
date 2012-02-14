<?php
/**
 *=-----------------------------------------------------------=
 * showweek.php
 *=-----------------------------------------------------------=
 *
 * Author: Marc Wandschneider:  2005-03-15
 *
 * This page shows the appointments for the current user
 * for the given week.  You specify a week by specifying a
 * date, and we'll figure out which week it is from there.
 *
 * y = year
 * m = month
 * d = day.
 *
 * If no GET parameters are given, then the current week
 * is used.
 */
ob_start();
$page_title = "Show Week's Appointments";

require_once('../libs/coreincs.inc');
require_once('../libs/pagetop.inc');


/**
 *=-----------------------------------------------------------=
 * convert_appts_to_markup
 *=-----------------------------------------------------------=
 * Takes an array of appointments and returns some markup
 * for them that we will use in our weekly view.  The
 * appointment has a hyperlink to the showappt.php page.
 *
 * Parameters:
 *  $in_appts       - array of appointments to convert
 *
 * Returns:
 *  string
 */
function convert_appts_to_markup($in_appts)
{
  $first = TRUE;
  $str = '<br/>';
  foreach ($in_appts as $appt)
  {
    /**
     * First the when:
     */
    if ($appt->StartTime->sameDay($appt->EndTime))
    {
      $time = $appt->StartTime->getTextTime() . ' - '
              . $appt->EndTime->getTextTime();
    }
    else
    {
      $time = $appt->StartTime->getTextDateTime() . ' - '
              . $appt->EndTime->getTextDateTIme();
    }

    /**
     * Then the what/where:
     */
    $title = $appt->Title;
    $location = $appt->Location;
    $aid = $appt->AppointmentID;
    if ($first)
      $first = FALSE;
    else
      $str .= '<hr size=\'1\'/>';
    $str .= <<<EOSTR
$time<br/><a class='apptDispLink' href='showappt.php?aid=$aid'>
$title</a><br/>($location)<br/>
EOSTR;
  }

  $str .= '<br/>';
  return $str;
}


/**
 * See what date information we have.
 */
$year = isset($_GET['y']) ? $_GET['y'] : intval(date('Y'));
$month = isset($_GET['m']) ? $_GET['m'] : intval(date('m'));
$day = isset($_GET['d']) ? $_GET['d'] : intval(date('d'));
if (!checkdate($month, $day, $year))
{
  throw new InvalidDateException();
}

/**
 * Figure out the first and last day in this week.
 */
$dt = new MyDateTime($year, $month, $day, 0, 0);
$first = $dt->topOfWeek();
$last = $dt->bottomOfWeek();

/**
 * With this information, we can then go and get the
 * appointments for the given week.
 */
$am = AppointmentManager::getInstance();
$appts = $am->getAppointments($g_userID, $first, $last);
if ($appts === NULL)
  $appts = array();

/**
 * Now, split these appointments up into the individual days.
 */
$printable_dates = array();
$day_appts = array();
$curday = $first;
for ($x = 0; $x < 7; $x++)
{
  $day_appts[$x] = array();
  foreach ($appts as $appt)
  {
    if ($curday->containedInDates($appt->StartTime, $appt->EndTime))
    {
      $day_appts[$x][] = $appt;
    }
  }

  /**
   * Get the printable name for this day, and then move
   * to the next day.
   */
  $printable_dates[$x] = $curday->getMonthDayText();
  $curday = $curday->nextDay();
}



/**
 * Print out the page title and links to let them go to the
 * next and previous months.
 */
$nextweek = $dt->addOneWeek();
$prevweek = $dt->subOneWeek();


echo <<<EONEXTPREV
<br/>
<h2 align='center'>
    Appoinments from {$printable_dates[0]}
        to {$printable_dates[6]}
</h2>
<br/>
<table width='100%' border='0' cellspacing='0' cellpadding='0'>
<tr>
  <td align='left' width='50%'>
    <a class='nextPrevLink'
       href='showweek.php?y={$prevweek->Year}&m={$prevweek->Month}&d={$prevweek->Day}'>
      &lt;&lt;Prev
    </a>
  </td>
  <td align='right'>
    <a class='nextPrevLink'
       href='showweek.php?y={$nextweek->Year}&m={$nextweek->Month}&d={$nextweek->Day}'>
      Next &gt;&gt;
    </a>
  </td>
</tr>
</table>
<br/>

EONEXTPREV;

/**
 * Now start dumping the appointments.
 */
echo <<<EOTABLE
<br/>
<table width='100%' border='1' cellspacing='0' cellpadding='0'
       class='apptTable'>
<tr>
  <td align='center' width='14%' class='apptWeekHeader'>
    Sunday<br/>{$printable_dates[0]}
  </td>
  <td align='center' width='14%' class='apptWeekHeader'>
    Monday<br/>{$printable_dates[1]}
  </td>
  <td align='center' width='14%' class='apptWeekHeader'>
    Tuesday<br/>{$printable_dates[2]}
  </td>
  <td align='center' width='14%' class='apptWeekHeader'>
    Wednesday<br/>{$printable_dates[3]}
  </td>
  <td align='center' width='14%' class='apptWeekHeader'>
    Thursday<br/>{$printable_dates[4]}
  </td>
  <td align='center' width='14%' class='apptWeekHeader'>
    Friday<br/>{$printable_dates[5]}
  </td>
  <td align='center' class='apptWeekHeader'>
    Saturday<br/>{$printable_dates[6]}
  </td>
</tr>
<tr>

EOTABLE;

/**
 * Okay, for each day, we'll dump the appointments that fall in
 * that day.
 */
for ($x = 0; $x < 7; $x++)
{
  /**
   * Get the dumpable information for the appts for that day.
   */
  if ($day_appts[$x] === NULL or
      (is_array($day_appts[$x]) and count($day_appts[$x]) == 0))
  {
    $str = "<br/>No Appointments Scheduled<br/>";
  }
  else
  {
    $str = convert_appts_to_markup($day_appts[$x]);

  }

  echo <<<EOTD
  <td align='center' valign='top'>$str</td>

EOTD;
}


echo <<<EOTABLE
</tr>
</table>

EOTABLE;


/**
 * Close and exit!
 */
require_once('../libs/appts/pagebottom.inc');
ob_end_flush();
?>
