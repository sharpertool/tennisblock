<?php
    include 'checkLogin.php';
    include '../lib/common.php';
    include '../inc/Schedule.php';
    include '../inc/errors.inc';
    
    if (!isset($username) or $username != 'kutenai') {
        header( "Location: member_availability.php" );
    }
    $schmgr = ScheduleManager::getInstance();
    if (isset($_SESSION['season'])) {
        $schmgr->setSeason($_SESSION['season']);
        $season = $_SESSION['season'];
    }
    $players = $schmgr->GetPlayers();
    
    # Clear out all current availability... This is sort of dangerous!!!
    echo "Set all available<br>";
    $schmgr->SetAllAvailable();
    echo "Done with that, now set those that are not available<br>";
    
    foreach ($_POST as $id => $value) {
        list($spid,$sdate) = split("_",$id);
        list($dummy,$pid) = split(":",$spid);
        list($dummy,$date) = split(":",$sdate);
        echo "$id Pid:$pid Date:$date Availability:$value<br>";
        $schmgr->SetUnavailable($pid,$date);
    }
    header( "Location: member_availability.php" );
?>