<?php
    include 'checkLogin.php';
    include '../lib/common.php';
    include '../inc/Schedule.php';
    include '../inc/errors.inc';

    // accept incoming URL parameter, but, adjust to a Friday...
    $timestamp = (isset($_GET['t'])) ? $_GET['t'] : time();
    $currdate = date("Y-m-d",$timestamp);

    $dates = array();
    $t = mktime(12,0,0,1,14,2011);
    $dates[] = $t;
    for ($x=0;$x<15;$x++) {
        $t = strtotime('+1 week', $t);
        $dates[] = $t;
    }
    
    $colspan = 6 + count($dates);
    
    $schmgr = ScheduleManager::getInstance();

    // output table header
    ob_start();
    $can_edit = False;
    if (isset($_SESSION['username']) and $_SESSION['username'] == 'kutenai') {
        $can_edit = True;
    }

    if ($can_edit) {
        echo '<form method="post" action="update_availability.php">';
    }
    $headers = array("Name","NTPR","email","Home","Cell","Work","Matches Played","Total Scheduled");
    echo "<table class=\"member_list\">\n";
    echo "<tr class=\"member_list_header\">\n";
    echo "<th class=\"member_list_top_header\" colspan=\"" . count($headers) . "\">\n";
    echo "Friday Night Block Members";
    echo "</th>\n";
    echo "</tr>\n";
    echo "<tr class=\"member_list_header_2\">\n";
    foreach ($headers as $header) {
        echo "<th>$header</th>\n";
    }
    echo "</tr>\n";

    #$future_date = date("Y-m-d",strtotime('+6 weeks',$timestamp));
    $future_date = $schmgr->LastBlockDate();
    $fd_ts = strtotime($future_date);
    $fd_ts = strtotime('+1 week', $fd_ts);
    $future_date = date("Y-m-d",$fd_ts);

    $players = $schmgr->GetPlayers();
    $count = 0;
    $match_count = $schmgr->GetMatchCount($currdate);
    $scheduled_matches = $schmgr->GetMatchCount($future_date);
    
    // output players
    foreach ($players as $player) {
        $count = $schmgr->GetPlayersCountByID($player->pid,$currdate);
        $count_sch = $schmgr->GetPlayersCountByID($player->pid,$future_date);
        echo '<tr class="members">';

        echo '<td class="name">' . $player->firstname . " " . $player->lastname . '</td>';
        echo '<td class="event">';
        echo number_format($player->NTRP,1);
        echo '</td>';
        echo '<td class="event">';
        echo $player->email;
        echo '</td>';
        echo '<td class="event">';
        echo $player->home;
        echo '</td>';
        echo '<td class="event">';
        echo $player->cell;
        echo '</td>';
        echo '<td class="event">';
        echo $player->work;
        echo '</td>';
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

    $GLOBALS['TEMPLATE']['title'] = "<h2>Member List for $season_text</h2>";
    $GLOBALS['TEMPLATE']['content'] = ob_get_clean();
    
    $GLOBALS['TEMPLATE']['extra_head'] = '<link rel="stylesheet" ' . 
        'type="text/css" href="css/members.css" title="Default"/>' .
        '<link rel="stylesheet" ' . 
        'type="text/css" href="css/members_cool.css" title="Cool"/>'
        ;
    
    include '../templates/template-page.php';
?>
