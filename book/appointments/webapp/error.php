<?php
/**
 * error.php
 *
 * Author: Marc Wandschneider:  2005-03-03
 *
 * This script is used to report unhandled errors in our
 * web application.  The user is typically sent here when
 * there is an unhandled error or an unhandled exception.
 *
 * In both cases, the session data has hopefully been primed
 * with data that we can use to print a more helpful message
 * for the user.
 */
ob_start();
$page_title = "Error";

require_once('../libs/errors.inc');
require_once('posterstore/session.inc');
require_once('../libs/pagetop.inc');

if (isset($_SESSION['exception']))
{
  $exc = $_SESSION['exception'];
  $msg = $exc->getMessage();
}
else if (isset($_SESSION['errstr']))
{
  $msg = $_SESSION['errstr'];
}
else if (!isset($_SESSION))
{
  $msg = <<<EOM
Unable to initialise the session.  Please verify
that the session data directory exists.
EOM;
}
else
{
  $msg = 'Unknown Error';
}

    //unset($_SESSION['exception']);
    //unset($_SESSION['errstr']);


?>

<h2 align='center'>Unexpected Error</h2>
<p align='center'>
  We are very sorry, but an unexpected error has occurred in
  the application.  This occurs either because a page was
  used improperly and visited directly instead of through the
  web site or because of a system error in the application.
  The website administrators have been
  notified and will look into the problem as soon as possible.
  We apologise for the inconvenience and kindly ask you to try
  again or try back again in a little while.
</p>
<p align='center'>
  Please click <a href='index.php'>here</a> to go back to the
  main page and continue working with our system.
</p>
<p align='center'>
  The error received was: <br/><br/>
  <b><?php echo $msg ?></b>
</p>


<?php

require_once('../libs/appts/pagebottom.inc');
ob_end_flush();
?>