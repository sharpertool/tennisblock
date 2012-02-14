<?php
/**
 * index.php
 *
 * Author: Marc Wandschneider:  2005-03-03
 *
 * This is the home page for this web site and drives our
 * simple appointment calendar system.
 */
ob_start();
$page_title = "Appointments System";

require_once('../libs/coreincs.inc');
require_once('../libs/pagetop.inc');

$am = AppointmentManager::getInstance();
$appts = $am->getPendingAppointments($g_userID, 5);

?>

<h2 align='center'>Welcome to the Appointment Manager</h2>
<p align='center'>
  This is a simple little demonstration appointment<br/>
  manager.  Please select an item from the menu above to<br/>
  either add a new appointment or view existing ones.<br/>
</p>
<br/>
<h2 align='center'>Your Next Five Appointments</h2>

<?php

if ($appts === NULL)
{
  echo <<<EOEMPTY
<p align='center'>
  You have no upcoming appointments.
</p>

EOEMPTY;
}
else
{
  /**
   * List the appointments.  Start the table.
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

require_once('../libs/appts/pagebottom.inc');
ob_end_flush();
?>
