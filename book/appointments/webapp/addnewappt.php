<?php
/**
 *=-----------------------------------------------------------=
 * addnewappt.php
 *=-----------------------------------------------------------=
 *
 * Author: Marc Wandschneider:  2005-03-15
 *
 * This page adds a new appointment into our system for the
 * current user.
 */
ob_start();
$page_title = "Create New Appointment";

require_once('../libs/coreincs.inc');
require_once('../libs/pagetop.inc');

$cur_year = intval(date('Y'));
$cur_month = intval(date('m'));
$cur_day = intval(date('d'));
$title = '';


/**
 * First, see if we were sent back here because of an input
 * error.
 */
if (isset($_SESSION['apptinfo']))
{
  $ai = &$_SESSION['apptinfo'];
  $title = $ai['title'];
  $location = $ai['location'];
  $syear = $ai['syear'];
  $smonth = $ai['smonth'];
  $sday = $ai['sday'];
  $stime = $ai['stime'];
  $eyear = $ai['eyear'];
  $emonth = $ai['emonth'];
  $eday = $ai['eday'];
  $etime = $ai['etime'];
  $desc = $ai['desc'];
}
else
{
  $title = '';
  $location = '';
  $syear = '';
  $smonth = '';
  $sday = '';
  $stime = '';
  $eyear = '';
  $emonth = '';
  $eday = '';
  $etime = '';
  $desc = '';
}

/**
 * Get the error message
 */
$msg = '';
if (isset($_GET['err']))
{
  switch ($_GET['err'])
  {
    case 'title':
      $msg = 'You must specify a title for the appointment';
      break;
    case 'sdate':
      $msg = 'The starting date for the appointment is not valid';
      break;
    case 'stime':
      $msg = 'The starting time for the appointment is not valid';
      break;
    case 'edate':
      $msg = 'The end date for the appointment is not valid';
      break;
    case 'dtime':
      $msg = 'The finish time for the appointment is not valid';
      break;
    case 'lesser':
      $msg = 'The end date and time for the appointment are before the start time!';
      break;
    case 'conflict':
      $msg = <<<EOM
Sorry, but there are already one or more appointments scheduled
at this time.
EOM;
      break;
  }

  if ($msg != '')
  {
    $msg = '<p align=\'center\'><br/><font class=\'errSmall\'>'
           . $msg .'</font><br/></p>';
  }
}

echo <<<EOHEADER
<h2 align='center'>Create New Appointment</h2>
$msg
EOHEADER;


echo <<<EOFORM

<form action='submitnewappt.php' method='POST'>
  <table align='center' width='80%' border='0' cellspacing='0'
         cellpadding='5' class='apptFormTable'>
  <tr>
    <td align='right' width='30%'>Title:&nbsp;</td>
    <td>
      <input type='text' size='40' name='title'
             value='$title'/>
    </td>
  </tr>
  <tr>
    <td align='right' width='30%'>Location:&nbsp;</td>
    <td>
      <input type='text' size='40' name='location'
             value='$location'/>
    </td>
  </tr>
  <tr>
    <td align='right' width='30%'>Start Date:&nbsp;</td>
    <td>
      <select name='syear'>

EOFORM;

/**
 * generate start year values.
 */
$init_year = ($syear === '') ? $cur_year : $syear;
for ($x = $cur_year; $x <= $cur_year + 5; $x++)
{
  $sel = ($init_year == $x) ? ' selected="selected"' : '';
  echo "        <option value='$x'$sel/>$x\n";
}
echo <<<EOFORM
      </select>
      - <select name='smonth'>

EOFORM;

/**
 * Generate Start Month Values ...
 */
$init_month = ($smonth === '') ? $cur_month : $smonth;
for ($x = 1; $x <= 12; $x++)
{
  $val = sprintf('%02d', $x);
  $sel = ($init_month == $x) ? ' selected="selected"' : '';
  echo "        <option value='$val'$sel/>$val\n";
}
echo <<<EOFORM
      </select>
      - <select name='sday'>

EOFORM;

/**
 * Generate start day values.
 */
$init_day = ($sday === '') ? $cur_day : $sday;
for ($x = 1; $x <= 31; $x++)
{
  $val = sprintf('%02d', $x);
  $sel = ($init_day == $x) ? ' selected="selected"' : '';
  echo "        <option value='$val'$sel/>$val\n";
}

echo <<<EOFORM
      </select>
    </td>
  </tr>

  <tr>
    <td align='right' width='30%'>Start Time:&nbsp;</td>
    <td>
      <select name='stime'>

EOFORM;

/**
 * Generate start time values.  The display values will be in
 * 12hr AM/PM time, but the value submitted to the server will
 * be in 24hr time for ease of processing later.
 */
for ($x = 0; $x <= 23; $x++)
{
  $ampm = ($x < 12) ? 'AM' : 'PM';
  $sel = ($x == 12) ? ' selected="selected"' : '';
  if ($x == 0)
    $print = 12;
  else if ($x > 12)
    $print = $x - 12;
  else
    $print = $x;

  echo <<<EOOPTION
        <option value='$x.00'$sel/>$print.00$ampm
        <option value='$x.30'/>$print.30$ampm

EOOPTION;
}

echo <<<EOFORM
      </select>
    </td>
  </tr>

  <tr>
    <td align='right' width='30%'>End Date:&nbsp;</td>
    <td>
      <select name='eyear'>

EOFORM;

/**
 * Generate end year values.
 */
$init_year = ($eyear === '') ? $cur_year : $eyear;
for ($x = $cur_year; $x <= $cur_year + 5; $x++)
{
  $sel = ($init_year == $x) ? ' selected="selected"' : '';
  echo "        <option value='$x'$sel/>$x\n";
}
echo <<<EOFORM
      </select>
      - <select name='emonth'>

EOFORM;

/**
 * Generate end date month values.
 */
$init_month = ($emonth === '') ? $cur_month : $emonth;
for ($x = 1; $x <= 12; $x++)
{
  $val = sprintf('%02d', $x);
  $sel = ($init_month == $x) ? ' selected="selected"' : '';
  echo "        <option value='$val'$sel/>$val\n";
}
echo <<<EOFORM
      </select>
      - <select name='eday'>

EOFORM;

/**
 * Generate end date day values.
 */
$init_day = ($eday === '') ? $cur_day : $eday;
for ($x = 1; $x <= 31; $x++)
{
  $val = sprintf('%02d', $x);
  $sel = ($init_day == $x) ? ' selected="selected"' : '';
  echo "        <option value='$val'$sel/>$val\n";
}

echo <<<EOFORM
      </select>
    </td>
  </tr>

  <tr>
    <td align='right' width='30%'>End Time:&nbsp;</td>
    <td>
      <select name='etime'>

EOFORM;

/**
 * Generate end time values.  The display values will be in
 * 12hr AM/PM time, but the value submitted to the server will
 * be in 24hr time for ease of processing later.
 */
for ($x = 0; $x <= 23; $x++)
{
  $ampm = ($x < 12) ? 'AM' : 'PM';
  $sel = ($x == 12) ? ' selected="selected"' : '';
  if ($x == 0)
    $print = 12;
  else if ($x > 12)
    $print = $x - 12;
  else
    $print = $x;

  echo <<<EOOPTION
        <option value='$x.00'/>$print.00$ampm
        <option value='$x.30'$sel/>$print.30$ampm

EOOPTION;
}

echo <<<EOFORM
      </select>
    </td>
  </tr>
  <tr>
    <td align='right' width='30%'>Description:</td>
    <td>
      <textarea name="desc" cols='40' rows='10' wrap='virtual'>$desc</textarea>
    </td>
  </tr>
  <tr>
    <td colspan='2' align='center'>
      <input type='submit' value='Create Appointment'/>
    </td>
  </tr>
  </table>
</form>


EOFORM;


require_once('../libs/appts/pagebottom.inc');
ob_end_flush();
?>
