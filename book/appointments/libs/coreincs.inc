<?php
/**
 *=-----------------------------------------------------------=
 * coreincs.inc
 *=-----------------------------------------------------------=
 * Author: Marc Wandschneider, 2005-03-15
 *
 * This file is what we will include at the top of each of our
 * pages and scripts for this web application.  That way,
 * instead of remembering to have to include n .inc pages,
 * just including this one takes care of all the rest for the
 * page author.
 *
 * This page also sets up the dummy $g_userID variable for
 * our system, since we will only support a single user for
 * now.  Otherwise, we would run some code to figure out who
 * was currently logged in....
 */
require_once('../libs/errors.inc');
require_once('../libs/session.inc'); // this starts the session
require_once('../libs/appointmentmanager.inc');

/**
 * We're 'cheating' in this simple application and not
 * actually tracking users.  While we've set up the database
 * architecture to support this, our sample application will
 * just always assume a user_id of 1.
 */
$g_userID = 1;

?>
