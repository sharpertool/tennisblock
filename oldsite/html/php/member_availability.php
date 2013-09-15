<?php
    include 'checkLogin.php';
    include 'lib/common.php';
    include 'inc/Schedule.php';
    include 'inc/errors.inc';
    
    ob_start();

    $schmgr = ScheduleManager::getInstance();

    $timestamp = (isset($_GET['t'])) ? $_GET['t'] : time();
    $currdate = date("Y-m-d",$timestamp);

    // Insert the first block date
    $dates = array();
    if ($season == '2012 Fall') {
        #hr, min, sec, mo, day, year
        $t = mktime(12,0,0,9,21,2012);
    }
    $dates[] = $t;
    $t = strtotime('+1 week', $t);
    $last_blk_date = $schmgr->LastBlockDate();
    $lbts = strtotime($last_blk_date);
    while ($t <= strtotime('+16hours',$lbts)) {
        $dates[] = $t;
        $t = strtotime('+1 week', $t);
        $ts = date('M d Y H:m',$t);
    }
    
    $colspan = 6 + count($dates);
    
    // output table header
    $can_edit = False;
    if (isset($_SESSION['username']) and $_SESSION['username'] == 'kutenai') {
        $can_edit = True;
    }

    if ($can_edit) {
        echo '<form method="post" action="update_availability.php">';
        echo '<input type=submit value="Submit Availability Changes">';
    }
    echo '<table class="member_list">';
    echo '<tr class="member_list_header"><th colspan="1">';
    echo 'Block Member';
    echo '</th>';
    $colspan = count($dates) + 2;
    echo '<th colspan=' . $colspan . '>Check if Unavailable</th>';
    echo '</tr>';
    echo '<tr class="member_list_header_2">';
    echo '<th class="name">Name</th>';
    foreach ($dates as $date) {
        if ($schmgr->IsHoldout($date)) {
            echo '<th class="date_holdout">';
        } else {
            echo '<th class="date">';
        }
        echo date('M d',$date);
        echo '</th>';
    }
    echo '<th>Played</th><th>Scheduled</th>';
    echo '</tr>';

    $future_date = $schmgr->LastBlockDate();
    $fd_ts = strtotime($future_date);
    $fd_ts = strtotime('+1 week', $fd_ts);
    $future_date = date("Y-m-d",$fd_ts);

    $players = $schmgr->GetPlayers();
    $match_count = $schmgr->GetMatchCount($currdate);
    $scheduled_matches = $schmgr->GetMatchCount($future_date);
    
    // output players
    foreach ($players as $player) {
        $count = $schmgr->GetPlayersCountByID($player->pid,$currdate);
        $count_sch = $schmgr->GetPlayersCountByID($player->pid,$future_date);

        echo '<tr class="members">';

        echo '<td class="name" id="name">' . $player->firstname . " " . $player->lastname . '</td>';
        
        $player->updateAvailability();
        foreach ($dates as $date) {
            if ($schmgr->IsHoldout($date)) {
                echo '<td class="date_holdout">';
            } else {
                echo '<td class="date">';
            }
            $input_box = "PID:" . $player->pid . " Date:" . date("Y-m-d",$date);
            
            $isScheduled = $player->isScheduled($date);
            
            if ($player->isAvailable($date)) {
                if ($can_edit) {
                    echo "<input type=\"checkbox\" name=\"$input_box\" value=\"on\">";
                }
                if ($isScheduled) {
                    echo "On";
                }
            } else {
                if ($can_edit) {
                    echo "<input checked type=\"checkbox\" name=\"$input_box\" value=\"off\">";
                } else {
                    echo "X ";
                }
                if ($isScheduled) {
                    echo "On";
                }
            }
            echo '</td>';

        }
        echo '<td class="event">';
        if ($match_count > 0) {
            $ratio = $count/$match_count;
        } else {
            $ratio = 0;
        }
        echo "$count of $match_count (" . sprintf("%4.1f",$ratio) . ")";
        echo '</td>';
        echo '<td class="event">';
        if ($scheduled_matches > 0) {
            $ratio = $count_sch/$scheduled_matches;
        } else {
            $ratio = 0;
        }
        echo "$count_sch of $scheduled_matches (" . sprintf("%4.2f",$ratio) . ")";
        echo '</td>';
        echo '</tr>';
    }
    echo '</table>';
    if ($can_edit) {
        echo '</form>';
    }

	$season_text = $schmgr->getSeasonText();
    echo "<center><h2>";

    $GLOBALS['TEMPLATE']['title'] = "<h2>Member Availability for $season_text</h2>";
    $GLOBALS['TEMPLATE']['content'] = ob_get_clean();
    
    $GLOBALS['TEMPLATE']['extra_head'] = '<link rel="stylesheet" ' . 
        'type="text/css" href="css/members.css" title="Default"/>' .
        '<link rel="stylesheet" ' . 
        'type="text/css" href="css/members_cool.css" title="Cool"/>'
        ;
    
    include '../templates/template-page.php';
?>
