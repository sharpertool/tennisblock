<?php
// uncomment below to turn off error reporting in production
// error_reporting(0);

// set time zone to use date/time functions without warnings
date_default_timezone_set('America/New_York');

// compensate for magic quotes if necessary
if (get_magic_quotes_gpc())
{
    function _stripslashes_rcurs($value)
    {
        return (is_array($value)) ?
            array_map('_stripslashes_rcurs', $value) : stripslashes($value);
    }
    $_GET = array_map('_stripslashes_rcurs', $_GET);
    $_POST = array_map('_stripslashes_rcurs', $_POST);
    // $_REQUEST = array_map('_stripslashes_rcurs', $_REQUEST);
    // $_COOKIE = array_map('_stripslashes_rcurs', $_COOKIE);
}
?>
