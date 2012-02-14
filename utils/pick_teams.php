<?php

    include '../inc/Schedule.php';
    require_once '../inc/Teams.php';
    include '../inc/errors.inc';

    $schmgr = ScheduleManager::getInstance();
    
    $matchid = 2059;
    try {
        $match = $schmgr->getMatchByID($matchid);
    } catch (DatabaseErrorException $e)
    {
        echo "Failed db " . $e->getmessage() . "\n";
    }
    
    $matches = array(2058,2059);
    
    foreach ($matches as $matchid) {
        $sets = array(1,2,3);
        $courts = array(1,2,3);
        Team::clearTeams($matchid);
        foreach ($sets as $set) {
            Team::resetPlayersTmp($matchid);
            foreach ($courts as $court) {
                $team = Team::pickTeam($matchid,$set,$court);
                // Insert this team intot the 'slots' table
                $team->insertRecord($matchid);
            }
        }
    }
    
    echo "Done Scheduling.\n\n";
?>