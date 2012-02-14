<?php
    include 'checkLogin.php';
    include '../lib/common.php';
    include '../inc/Schedule.php';
    include '../inc/errors.inc';

    // accept incoming URL parameter, but, adjust to a Friday...
    $timestamp = (isset($_GET['t'])) ? $_GET['t'] : time();
    $currdate = date("Y-m-d",$timestamp);

    $dates = array();
    $t = mktime(12,0,0,9,26,2008);
    $dates[] = $t;
    for ($x=0;$x<15;$x++) {
        $t = strtotime('+1 week', $t);
        $dates[] = $t;
    }
    
    $colspan = 6 + count($dates);
    
    $schmgr = ScheduleManager::getInstance();
    
    // output table header
    ob_start();
    echo '<a href="index.php">Home</a><br>';
    $can_edit = False;
    if (isset($_SESSION['username']) and $_SESSION['username'] == 'kutenai') {
        $can_edit = True;
    }

    if ($can_edit) {
        echo '<form method="post" action="update_availability.php">';
    }
    echo '<table id="member_list">';
    echo '<tr id="member_list_header"><th colspan="7">';
    echo 'Friday Night Block Members';
    echo '</th>';
    echo '</tr>';
    echo '<tr id="member_list_header_2">';
    echo '<th >Name</th><th>NTRP</th><th>email</th><th>Home</th><th>Cell</th><th>work</th><th>Plays</th>';
    echo '</tr>';

    $players = $schmgr->GetPlayers();
    $count = 0;
    
    // output players
    foreach ($players as $player) {
        $count = $schmgr->GetPlayersCountByID($player->pid,$currdate);
        echo '<tr id="members">';

        echo '<td class="name" id="name">' . $player->firstname . " " . $player->lastname . '</td>';
        echo '<td class="event" id="NTRP">';
        echo $player->NTRP;
        echo '</td>';
        echo '<td class="event" id="email">';
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
        echo $count;
        echo '</td>';
    }
    echo '</table>';
    if ($can_edit) {
        echo '</form>';
    }
    
    $GLOBALS['TEMPLATE']['title'] = "<h2>Member List</h2>";
    $GLOBALS['TEMPLATE']['content'] = ob_get_clean();
    
    $GLOBALS['TEMPLATE']['extra_head'] = '<link rel="stylesheet" ' . 
        'type="text/css" href="css/members.css" title="Default"/>' .
        '<link rel="stylesheet" ' . 
        'type="text/css" href="css/members_cool.css" title="Cool"/>'
        ;
    
    include '../templates/template-page.php';
?>
