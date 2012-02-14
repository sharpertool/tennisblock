<?php
    include 'checkLogin.php';
    include '../lib/common.php';
    include '../inc/Schedule.php';
    include '../inc/Teams.php';
    include '../inc/errors.inc';
    
    ob_start();
    echo "here";
    // accept incoming URL parameter, but, adjust to a Friday...
    $timestamp = (isset($_GET['t'])) ? $_GET['t'] : time();
    $d = date("Y-m-d G:i",$timestamp);
    //echo "Timestamp $timestamp<br>Time now is $d<br>";

    // Adjust to the next friday.
    $gdate = getdate($timestamp);
    $wday = $gdate['wday'];
    if ($wday != 5) {
        $timestamp = strtotime("next Friday+12 hours", $timestamp);
    }
    $d = date("Y-m-d G:i",$timestamp);
    ///echo "Wday is $wday Adjusted time now is $d<br>";
    // determine useful aspects of the requested month
    list($month, $day, $year) = explode('/', date('m/d/Y', $timestamp));
    $first_day_of_month = date('w', mktime(12, 0, 0, $month, 1, $year));
    $total_days = date('t', $timestamp);

    // output table header
    $can_edit = False;
    $show_slots = False;
    if (isset($_SESSION['username']) and $_SESSION['username'] == 'kutenai') {
        $can_edit = True;
        $show_slots = True;
    }
    // Put the User list in the first row of a table.
    echo '<table id = "match_calendar_top">';
    if ($can_edit) {
        echo '<tr><td>';
        echo '<form method="post" action="_pick_team.php">';
        echo '<input type=submit value="Pick Teams">';
        echo "<input type=hidden name=\"timestamp\" value=$timestamp>";
        echo '</form>';
        //echo '</td><td>';
        echo '<form method="post" action="_schedule.php">';
        echo '<input type=submit name="schedule" value="Schedule">';
        echo '<input type=submit name="clear" value="Clear Schedule">';
        echo "<input type=hidden name=\"timestamp\" value=$timestamp>";
        echo '</form>';
        echo "</td></tr>";
    }
    echo '<tr><td>';
    echo '<a href="index.php">Home</a><br>';
    $schmgr = ScheduleManager::getInstance();
    list($matchid,$players) = $schmgr->GetPlayersByDate($timestamp);
    if ($can_edit) {
        echo "<form method=\"post\" action=\"change_schedule.php?XDEBUG_SESSION_START=fnt\">\n";
        echo '<input type=submit name="update" value="Update Scheduled Players">';
        echo "<input type=hidden name=\"matchid\" value=$matchid>";
        echo "<input type=hidden name=\"timestamp\" value=$timestamp>";
    }
    echo '<table id="match_calendar" border=1>';
    echo '<tr id="match_calendar_header"><th colspan="2">';
    echo '<a href="'. htmlspecialchars($_SERVER['PHP_SELF']) . '?t=' .
        strtotime('-1 week', $timestamp) . '">&lt;</a> &nbsp;';
    echo date('l F d, Y', $timestamp);
    echo '&nbsp; <a href="'. htmlspecialchars($_SERVER['PHP_SELF']) . '?t=' .
        strtotime('+1 week', $timestamp) . '">&gt;</a>';
    echo '</th></tr>';

    echo "<td>";
    echo "</td>";
    
    $pids = array();
    foreach ($players as $player) {
        $pids[] = $player->pid;
    }
    
    $all_players = $schmgr->GetAllPlayers();
    
    // output players
    foreach ($players as $player) {
        echo "<tr><td class=\"name\">\n";

        if ($can_edit) {
            echo "<select name=\"schedid:" . $player->schedid . "\">\n";
            foreach ($all_players as $aplayer) {
                # Only add players of the same gender to the change list.
                if ($aplayer->gender == $player->gender) {
                    if ($aplayer->pid == $player->pid) {
                        echo "<option value =\"" . $aplayer->pid . "\" "; // Start an option
                        echo "selected=\"selected\">";
                        echo $aplayer->firstname . " " . $aplayer->lastname . "</option>\n";
                    } else {
                        # Don't add subs if they are already playing.
                        if (!in_array($aplayer->pid,$pids)) {
                            echo "<option value =\"" . $aplayer->pid . "\" "; // Start an option
                            echo ">";
                            echo $aplayer->firstname . " " . $aplayer->lastname . "</option>\n";
                        }
                    }
                }
            }
            echo "</select>\n";
        } else {
            echo $player->firstname . " " . $player->lastname;
        }
        echo "</td></tr>";
    }
    if ($can_edit) {
        echo "</form>\n";
    }
    echo '</table>';
    
    // End the first row of the top level table
    echo '</td></tr>';
    
    // Start the next row
    echo '<tr><td>';

    if ($show_slots) {
        //echo '<br><hr>';
        echo "<table border=1>\n";
        echo "<th rowspan=2>Set</th><th rowspan=2>Court</th><th colspan='2'>Couple one</th><th colspan=2>Couple two</th>\n";
        echo "<tr><th>Guy</th><th>Girl</th><th>Guy</th><th>Girl</th></tr>\n";
        // Get the list of players and their matches.
        $sets = array(1,2,3);
        $courts = array(1,2,3);
        $matchid = $schmgr->getMatchid($timestamp);;
        foreach ($sets as $set) {
            foreach ($courts as $court) {
                echo "<tr>";
                echo "<td>$set</td><td>$court</td>\n";
                $team = Team::getTeam($matchid,$set,$court);
                if ($team != NULL and $team->team != NULL) {
                    foreach (array('tapa','tapb','tbpa','tbpb') as $p) {
                        if (array_key_exists($p,$team->team)) {
                            echo "<td>" . $team->team[$p]->firstname . " " . $team->team[$p]->lastname . "</td>\n";
                        } else {
                            echo "<td>??</td>\n";
                        }
                    }
                }
                echo "</tr>\n";
            }
        }
        echo "</table>\n";
    }
    
    // End the second row
    echo '</td></tr>';
    // And the top level table
    echo '</table>';
    
    echo "<br><br>";
    
    $GLOBALS['TEMPLATE']['title'] = "<h3>Match Schedule</h3>";
    $GLOBALS['TEMPLATE']['content'] = ob_get_clean();
    
    $GLOBALS['TEMPLATE']['extra_head'] = '<link rel="stylesheet" ' . 
        'type="text/css" href="css/calendar.css"/>';
    
    include '../templates/template-page.php';
?>
