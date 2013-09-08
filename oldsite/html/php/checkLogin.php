<?php
    //start the session
    session_start();
    
    //check to make sure the session variable is registered
    if(!session_is_registered('username')){
        //the session variable isn't registered, send them back to the login page
        header( "Location: login.html" );
    }
    date_default_timezone_set('America/MST');
?>