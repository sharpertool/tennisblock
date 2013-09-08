<?php

    include 'checkLogin.php';
    include 'inc/Schedule.php';
    require_once 'inc/Teams.php';
    include 'inc/errors.inc';
    //include 'inc/pick_teams_utils.php';
    include 'inc/TeamGen.php';
    
    date_default_timezone_set('America/Denver');
    
    $schmgr = ScheduleManager::getInstance();
    if (isset($_SESSION['season'])) {
        $schmgr->setSeason($_SESSION['season']);
        $season = $_SESSION['season'];
    }
    
    $timestamp = (isset($_POST['timestamp'])) ? $_POST['timestamp'] : time();

    if (isset($_POST['matchid'])) {
        $matchid =  $_POST['matchid'];
    } elseif (isset($_POST['timestamp'])) {
        //echo "Timestamp sent to us as $timestamp<br/>\n";
        $d = date("Y-m-d G:i",$timestamp);
        //echo "Date for this is $d<br>";
        $matchid = $schmgr->getMatchID($timestamp);
        //echo "The match is is $matchid\n<br/>";
    }
    if (!isset($matchid)) {
        //echo "Sorry, could not determine the match id<br/>";
    } else {
        $usePython = true;
        if ($usePython) {
            $court_count = $schmgr->getCourtCount();
            $python = "/usr/bin/python";
            $cmdline = "$python /var/www/tennis/friday_block/scripts/PickTeams.py -n -m $matchid -c $court_count -f /tmp/pickteams.log 2>&1";
            $retval;
            //system($cmdline,$retval);
            /* Add redirection so we can get stderr. */
            $handle = popen($cmdline, 'r');
            echo "'$handle'; " . gettype($handle) . "\n";
            $read = fread($handle, 2096);
            echo $read;
            pclose($handle);
            echo "Teams Picked..";
        } else {
            try {
                $match = $schmgr->getMatchByID($matchid);
                $sets = array(1,2,3);
                $court_count = $schmgr->getCourtCount();
                $courts = array();
                for ($c = 1;$c<=$court_count;$c++) {
                    $courts[] = $c;
                }
                Team::clearTeams($matchid);
                Team::resetTmpPlayers($matchid);
                Team::resetTmpCouples($matchid);
                
                if (isset($_POST['pick'])) {
                    list($men,$women) = Team::getPlayers();
                    $t = new TeamGen($court_count,$men,$women);
                    $seqs = $t->generateSetSequences();
                    foreach ($sets as $set) {
                        $seq = $seqs[$set-1];
                        $ms = $seq[0];
                        $fs = $seq[1];
                        foreach ($courts as $court) {
                            $x = ($court-1)*2;
                            $team = new Team($set,$court);
                            $team->setPlayers(array($men[$ms[$x]],$women[$fs[$x]]),array($men[$ms[$x+1]],$women[$fs[$x+1]]));
                            $team->insertRecord($matchid);
                        }
                    }
                }
            //echo "Done Scheduling.<br/>\n\n";
            } catch (DatabaseErrorException $e)
            {
                echo "Failed db " . $e->getmessage() . "\n<br/>";
            }
        }
    }
    header( "Location: match_calendar.php?t=$timestamp" );

    //echo "Done with script.<br/>\n\n";
?>
