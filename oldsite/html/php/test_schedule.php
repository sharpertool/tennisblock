<?php
    
    include 'inc/Schedule.php';
    include 'inc/errors.inc';

    echo phpinfo();
    $schmgr = ScheduleManager::getInstance();
    
    echo "Get match by ID\n";
    try {
        $match = $schmgr->getMatchByID(2058);
    } catch (DatabaseErrorException $e)
    {
        echo "Failed db " . $e->getmessage() . "\n";
    }
    
    echo "Got the match!\n";
    echo var_export($match);
    
    $couples = $schmgr->GetNextGroup();
    
    echo "\n\n";
    foreach ($couples as $couple ) {
        echo "Couple: $couple->name\n";
    }
    #echo var_export($couples);

?>
