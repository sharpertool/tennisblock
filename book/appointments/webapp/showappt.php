<?php
/**
 * showappt.php
 *
 * Author: Marc Wandschneider:  2005-03-15
 *
 * This page shows the details for a particular appointment.
 * The appointment is specified in the "aid" parameter to
 * this page.  It is an error to not specify this or specify
 * an invalid appointment_id.
 */
ob_start();
$page_title = "Appointment Details";

require_once('../libs/coreincs.inc');
require_once('../libs/pagetop.inc');

/**
 *  Get the Appointment ID.
 */
if (!isset($_GET['aid']))
{
  throw new InvalidAppointmentExceptoin();
}
else
{
  $aid = intval($_GET['aid']);
}


/**
 * Get the Appointment details.  This will fail if:
 *
 * - the appointment id is invalid.
 * - the appointment owner is not the current userid.
 */
$am = AppointmentManager::getInstance();
$appt = $am->getAppointmentDetails($g_userID, $aid);

/**
 * Get the relevant information and then display it.
 */
$start = $appt->StartTime->getTextDateTime();
$end = $appt->EndTime->getTextDateTime();
$desc = ereg_replace('\n', '<br/>', $appt->Description);

echo <<<EOTABLE
<h2 align='center'>Appointment Details</h2>
<table width='50%' align='center' border='1' cellspacing='0'
       cellpadding='4' class='apptDispTable'>
<tr>
  <td width='30%' class='apptDispHeader'> Title: </td>
  <td> {$appt->Title} </td>
</tr>
<tr>
  <td width='30%' class='apptDispHeader'> Location: </td>
  <td> {$appt->Location} </td>
</tr>
<tr>
  <td width='30%' class='apptDispHeader'> Start Time: </td>
  <td> {$start} </td>
</tr>
<tr>
  <td width='30%' class='apptDispHeader'>End Time: </td>
  <td> {$end} </td>
</tr>
<tr>
  <td width='30%' class='apptDispHeader'> Description: </td>
  <td> {$desc} </td>
</tr>
</table>


EOTABLE;


/**
 * Close and exit!
 */
require_once('../libs/appts/pagebottom.inc');
ob_end_flush();
?>
