<?php

    include 'checkLogin.php';
    include '../inc/Schedule.php';
    require_once '../inc/Teams.php';
    include '../inc/errors.inc';
    
    $schmgr = ScheduleManager::getInstance();
    
    if (isset($_POST['matchid'])) {
        $matchid =  $_POST['matchid'];
    } elseif (isset($_POST['timestamp'])) {
        $timestamp = $_POST['timestamp'];
        //echo "Timestamp sent to us as $date<br/>\n";
        $matchid = $schmgr->getMatchID($timestamp);
        //echo "The match is is $matchid\n<br/>";
    }
    if (!isset($matchid)) {
        echo "Sorry, could not determine the match id<br/>";
    } else {
        try {
            $schmgr->clearScheduleByID($matchid);
            if (isset($_POST['clear'])) {
                // If I clear the schedule, I need to clear the teams also
                $schmgr->clearSlotsByID($matchid);
            }
            if (isset($_POST['schedule'])) {
                $couples = $schmgr->getNextGroup($timestamp);
                $schmgr->AddCouplesToSchedule($matchid,$couples);
                // We changed the couples, so clear the slots
                $schmgr->clearSlotsByID($matchid);
            }
        } catch (DatabaseErrorException $e)
        {
            //echo "Failed db " . $e->getmessage() . "\n<br/>";
        }
    }
    header( "Location: http://fridaynighttennis.deepbondi.net/_match_calendar.php?t=$timestamp" );
?>