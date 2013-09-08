<?php

    include 'checkLogin.php';
    include '../inc/Schedule.php';
    require_once '../inc/Teams.php';
    include '../inc/errors.inc';
    
    $schmgr = ScheduleManager::getInstance();
    if (isset($_SESSION['season'])) {
        $schmgr->setSeason($_SESSION['season']);
        $season = $_SESSION['season'];
    }
    
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
    header( "Location: match_calendar.php?t=$timestamp" );
?>