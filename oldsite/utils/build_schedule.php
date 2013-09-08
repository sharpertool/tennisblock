<?php

    include '../inc/Schedule.php';
    include '../inc/errors.inc';

    $schmgr = ScheduleManager::getInstance();
    
    echo "Get match by ID\n";
    try {
        $match = $schmgr->getMatchByID(2058);
    } catch (DatabaseErrorException $e)
    {
        echo "Failed db " . $e->getmessage() . "\n";
    }
    
    $matches_to_schedule = $schmgr->GetUnsheduledMathces();
    $i = 0;
    foreach ($matches_to_schedule as $match) {
        $couples = $schmgr->GetNextGroup($match->Date);
        $schmgr->AddCouplesToSchedule($match,$couples);
        $i++;
        if ($i == 2) {
            break;
        }
    }
    
    echo "Done Scheduling.\n\n";
?>