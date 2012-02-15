<?php
    include '../inc/Schedule.php';
    include '../inc/TeamGen.php';
    require_once '../inc/Teams.php';
    
    $schmgr = ScheduleManager::getInstance();

    $matchid = 2083;    
    Team::clearTeams($matchid);
    Team::resetTmpPlayers($matchid);
    Team::resetTmpCouples($matchid);
    list($men,$women) = Team::getPlayers();
    $t = new TeamGen(4,$men,$women);
    $seqs = $t->generateSetSequences();
    echo "Finished generating sequences\n";
    $t->DisplaySeq();
    $t->ShowStats();
?>