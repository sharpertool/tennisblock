<?php
/**
 *=-----------------------------------------------------------=
 * showmonth.php
 *=-----------------------------------------------------------=
 * Author: Marc Wandschneider:  2005-03-15
 *
 * This page shows the appointments for the current user
 * for the given month.  You specify a month by specifying a
 * date, and we'll figure out which month it is from there.
 *
 * y = year
 * m = month
 * d = day.
 *
 * If no GET parameters are given, then the current month
 * is used.
 */
ob_start();
$page_title = "Monthly View of Appointments";

require_once('../libs/coreincs.inc');
require_once('../libs/pagetop.inc');

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
 * Figure out the start and end days for this month, as
 * well as how many days there are.
 */
$dt = new MyDateTime($year, $month, $day, 0, 0);
$first = $dt->topOfMonth();
$last = $dt->bottomOfMonth();
$days_in_month = $last->Day;
$first_day_of_week = $first->getDayOfWeekInt();
$month_name = $first->getMonthName();


/**
 * Print out the page title and links to let them go to the
 * next and previous months.
 */
$nextmo = ($month == 12) ? 1 : $month + 1;
$nextyear = ($nextmo == 1) ? $year + 1 : $year;
$prevmo = ($month == 1) ? 12 : $month - 1;
$prevyear = ($prevmo == 12) ? $year - 1 : $year;
if ($prevyear == 1969)
{
  $prevmo = 1;
  $prevyear = 1970;
}
if ($nextyear == 2038)
{
  $nextmo = 12;
  $nextyear = 2037;
}

echo <<<EONEXTPREV
<br/>
<h2 align='center'>
    Appointments for $month_name, $year
</h2>
<br/>
<table width='100%' border='0' cellspacing='0' cellpadding='0'>
<tr>
  <td align='left' width='50%'>
    <a class='nextPrevLink'
       href='showmonth.php?y=$prevyear&m=$prevmo&d=1'>
      &lt;&lt;Prev
    </a>
  </td>
  <td align='right'>
    <a class='nextPrevLink'
       href='showmonth.php?y=$nextyear&m=$nextmo&d=1'>
      Next &gt;&gt;
    </a>
  </td>
</tr>
</table>
<br/>

EONEXTPREV;


/**
 * With this information, we can then go and get the
 * appointments for the given month.
 */
$am = AppointmentManager::getInstance();
$appts = $am->getAppointments($g_userID, $first, $last);
if ($appts === NULL)
  $appts = array();

/**
 * Now, split these appointments up into the individual days.
 * Appointments spanning multiple days are put in multiple
 * buckets.
 */
$day_appts = array();
$curday = $first;
for ($x = 0; $x < $days_in_month; $x++)
{
  $day_appts[$x] = array();
  foreach ($appts as $appt)
  {
    if ($curday->containedInDates($appt->StartTime, $appt->EndTime))
    {
      $day_appts[$x][] = $appt;
    }
  }

  $curday = $curday->nextDay();
}

/**
 * Now start dumping the month.
 */
echo <<<EOTABLE
<table width='100%' border='1' cellspacing='0' cellpadding='0'
       class='apptTable'>
<tr>
  <td align='center' width='14%' class='apptMonthHeader'>
    Sunday
  </td>
  <td align='center' width='14%' class='apptMonthHeader'>
    Monday
  </td>
  <td align='center' width='14%' class='apptMonthHeader'>
    Tuesday
  </td>
  <td align='center' width='14%' class='apptMonthHeader'>
    Wednesday
  </td>
  <td align='center' width='14%' class='apptMonthHeader'>
    Thursday
  </td>
  <td align='center' width='14%' class='apptMonthHeader'>
    Friday
  </td>
  <td align='center' class='apptMonthHeader'>
    Saturday
  </td>
</tr>
<tr>

EOTABLE;

$current_day = 1;
$dumped = 0;

/**
 * First, fill in any spaces until the 1st of the month.
 */
for ($x = 0; $x < $first_day_of_week; $x++)
{
  echo "<td>&nbsp;</td>\n";
}
$dumped = $first_day_of_week;

/**
 * Now dump out all the days, making sure to wrap every
 * 7 days.
 */
while ($current_day <= $days_in_month)
{
  if (($dumped % 7) == 0)
  {
    echo "</tr>\n<tr/>\n";
  }

  /**
   * If there are any appts on a given day, make it a nice
   * link so the user can click on the day and see what
   * appointments there are ...  Otherwise, just print the
   * day.
   */
  if (count($day_appts[$current_day - 1]) == 0)
  {
    echo <<<EOTD
  <td align='center' valign='center'>
    <br/>$current_day<br/><br/>
  </td>

EOTD;
  }
  else
  {
    echo <<<EOLINK
  <td align='center' valign='center' class='dateWithAppts'>
    <br/><a class='apptDispLink'
      href='showday.php?y={$first->Year}&m={$first->Month}&d=$current_day'>
      $current_day
    </a><br/><br/>
  </td>

EOLINK;
  }

  $current_day++;
  $dumped++;
}

/**
 * Now close it off with any trailing blank slots.
 */
while ($dumped % 7 != 0)
{
  echo "<td>&nbsp;</td>\n";
  $dumped++;
}

echo <<<EOTABLE
</tr>
</table>

EOTABLE;

/**
 * Clean up and exit!
 */
require_once('../libs/appts/pagebottom.inc');
ob_end_flush();
?>
