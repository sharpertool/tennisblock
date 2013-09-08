<?php

    include 'checkLogin.php';
    include '../inc/Schedule.php';
    require_once '../inc/Teams.php';
    include '../inc/errors.inc';
    
    #echo phpinfo();
    
    $schmgr = ScheduleManager::getInstance();
    
    if (isset($_POST['update'])) {
        # Update the schedules.
        if (isset($_POST['matchid'])) {
            $matchid =  $_POST['matchid'];
            while (list($key,$value) = each($_POST)) {
                if (preg_match("/schedid:(\d+)/",$key,$matches)) {
                    $schedid = $matches[1];
                    $pid = $value;
                    //echo "Updating schedule $schedid with $pid<br>\n";
                    $schmgr->UpdateSchedule($schedid,$pid);
                } else {
                    //echo "Post key $key Value $value<br>";
                }
            }
        }
    }
    if (isset($_POST['timestamp'])) {
        $timestamp = $_POST['timestamp'];
        header( "Location: match_calendar.php?t=$timestamp" );
    } else {
        header( "Location: match_calendar.php" );
    }
?>