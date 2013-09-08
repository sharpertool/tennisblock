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
    //ob_start();
    $page_title = "Error";
    
    require_once('../inc/errors.inc');

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
    
    /**
     * Make sure that the next time an error occurs, we reset
     * these error data.
     */
    if (isset($_SESION['exception'])) {
        unset($_SESSION['exception']);
    }
    if (isset($_SESSION['errstr'])) {
        unset($_SESSION['errstr']);
    }
?>
    
    <h2 align='center'>Unexpected Error</h2>
    <p align='left'>
        Sorry, but something is wrong.. I hate to dump an error out at you,
        but it is probably better then just crashing.. I'll look into it as soon
        as I can. Try again in case that resovles it, but if it keeps happening,
        then please let me know so I can try and fix it.
    </p>
    <p align='center'>
      Please click <a href=''>here</a> to go back to the
      main page and try again.
    </p>
    <p align='center'>
      The error received was: <br/><br/>
      <b><?php echo $msg ?></b>
    </p>
    
    
<?php
   // ob_end_flush();
?>