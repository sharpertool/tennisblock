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
        //echo "Timestamp sent to us as $timestamp<br/>\n";
        $d = date("Y-m-d G:i",$timestamp);
        //echo "Date for this is $d<br>";
        $matchid = $schmgr->getMatchID($timestamp);
        //echo "The match is is $matchid\n<br/>";
    }
    if (!isset($matchid)) {
        //echo "Sorry, could not determine the match id<br/>";
    } else {
        try {
            $match = $schmgr->getMatchByID($matchid);
            $sets = array(1,2,3);
            $courts = array(1,2,3);
            Team::clearTeams($matchid);
            foreach ($sets as $set) {
                Team::resetTmpPlayers($matchid);
                foreach ($courts as $court) {
                    $team = Team::pickTeam($matchid,$set,$court);
                    // Insert this team intot the 'slots' table
                    $team->insertRecord($matchid);
                }
            }
        //echo "Done Scheduling.<br/>\n\n";
        } catch (DatabaseErrorException $e)
        {
            echo "Failed db " . $e->getmessage() . "\n<br/>";
        }
        
    }
    header( "Location: http://fridaynighttennis.deepbondi.net/match_calendar.php?t=$timestamp" );

    //echo "Done with script.<br/>\n\n";
?>