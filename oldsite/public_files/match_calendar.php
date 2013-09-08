<?php
    include 'checkLogin.php';
    include '../lib/common.php';
    include '../inc/Schedule.php';
    include '../inc/Teams.php';
    include '../inc/errors.inc';
    
    ob_start();

    $schmgr = ScheduleManager::getInstance();
    if (isset($_SESSION['season'])) {
        $schmgr->setSeason($_SESSION['season']);
    } else {
        $schmgr->setSeason("2012 Fall");
    }
    
    $firstdate = $schmgr->getFirstMatchDate();

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
    
    // $d is now the next friday.. if this date is earlier then the first match date, use
    // the first match date.
    if ($d < $firstdate) {
        $timestamp = strtotime($firstdate);
        $timestamp = strtotime("+12 hours", $timestamp);
        $gdate = getdate($timestamp);
        $d = date("Y-m-d G:i",$timestamp);
    }
    while ($schmgr->IsHoldout($timestamp)) {
        $timestamp = strtotime("+7 days", $timestamp);
        $gdate = getdate($timestamp);
        $d = date("Y-m-d G:i",$timestamp);
    }
    
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
    
    list($matchid,$players) = $schmgr->GetPlayersByDate($timestamp);
    $matchid = $schmgr->getMatchID($timestamp);
    $pids = array();
    foreach ($players as $player) {
        $pids[] = $player->pid;
    }
    
    $all_players = $schmgr->GetAllPlayers($timestamp);
    
    if ($can_edit) {
        echo "<table>\n";
        echo '<tr>';
        echo '<td>';
        echo '<form method="post" action="pick_team.php">';
        echo '<input type=submit name="pick" value="Pick Teams">';
        echo "<input type=hidden name=\"matchid\" value=$matchid>";
        echo '<input type=submit name="clear" value="Clear Teams">';
        echo "<input type=hidden name=\"timestamp\" value=$timestamp>";
        echo '</form>';
        //echo '</td><td>';
        echo '<form method="post" action="schedule.php">';
        echo '<input type=submit name="schedule" value="Schedule">';
        echo "<input type=hidden name=\"matchid\" value=$matchid>";
        echo '<input type=submit name="clear" value="Clear Schedule">';
        echo "<input type=hidden name=\"timestamp\" value=$timestamp>";
        echo '</form>';
        echo "<form method=\"post\" action=\"build_play_sheet.php\">\n";
        echo '<input type=submit name="build" value="Build Play Sheet">';
        echo "<input type=hidden name=\"matchid\" value=$matchid>";
        echo "<input type=hidden name=\"timestamp\" value=$timestamp>";
        echo "</form>\n";
        echo "</td></tr>";
        echo "</table>\n";

        $matchidTmp = $schmgr->getMatchID($timestamp);
    }
    // Put the User list in the first row of a table.
    if ($can_edit) {
        echo '<table class = "match_calendar_top">';
        echo '<tr><td>';
        echo "<form method=\"post\" action=\"change_schedule.php\">\n";
        echo '<input type=submit name="update" value="Update Scheduled Players">';
        echo "<input type=hidden name=\"matchid\" value=$matchid>";
        echo "<input type=hidden name=\"timestamp\" value=$timestamp>";
        echo "</tr></td>\n";
        echo "</table>\n";
    }
    echo '<table class="match_calendar" border=1>';
    echo '<tr class="match_calendar"><th class=match_calendar" colspan="2">';
    $prev_week = strtotime('-1 week', $timestamp);
    while ($schmgr->IsHoldout($prev_week)) {
        $prev_week = strtotime('-1 week',$prev_week);
    }
    if ($schmgr->getMatchID($prev_week) != NULL) {
        echo '<a href="'. htmlspecialchars($_SERVER['PHP_SELF']);
        echo "?t=$prev_week\">&lt;</a> &nbsp;";
    }
    
    # This date
    echo date('l F d, Y', $timestamp);
    
    // Get the next non-hold out week. But.. if that week is not a valid match,
    // then this is the end of the block, and don't add the right-arrow at all.
    $next_week = strtotime('+1 week', $timestamp);
    while ($schmgr->IsHoldout($next_week)) {
        $next_week = strtotime('+1 week', $next_week);
    }
    if ($schmgr->getMatchId($next_week) != NULL) {
        echo '&nbsp; <a href="'. htmlspecialchars($_SERVER['PHP_SELF']) . '?t=';
        echo "$next_week\">&gt;</a>";
    }
    echo '</th></tr>';

    // output players
    foreach ($players as $player) {
        echo "<tr class=\"match_calendar\"><td class=\"match_calendar\">\n";

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
    echo "</form>\n";
    
    // End the first row of the top level table
    echo '</td></tr></table>';
    
    if ($show_slots) {
        //echo '<br><hr>';
        echo "<table border=1>\n";
        echo "<th rowspan=2>Set</th><th rowspan=2>Court</th><th colspan='3'>Couple one</th><th colspan=3>Couple two</th>\n";
        echo "<tr><th>Guy</th><th>Girl</th><th>Comb</th><th>Guy</th><th>Girl</th><th>Comb</th><th>Diff</th></tr>\n";
        // Get the list of players and their matches.
        $sets = array(1,2,3);
        $court_count = $schmgr->getCourtCount();
        $courts = array();
        for ($c = 1;$c<=$court_count;$c++) {
            $courts[] = $c;
        }
        $matchid = $schmgr->getMatchid($timestamp);
        if ($matchid) {
            foreach ($sets as $set) {
                foreach ($courts as $court) {
                    echo "<tr>";
                    echo "<td>$set</td><td>$court</td>\n";
                    $team = Team::getTeam($matchid,$set,$court);
                    if ($team != NULL and $team->team != NULL) {
                        $cntrp_teama = 0;
                        foreach (array('tapa','tapb') as $pos) {
                            if (array_key_exists($pos,$team->team)) {
                                $p =  $team->team[$pos];
                                $s = sprintf("%s %s (%3.2f)",$p->firstname,$p->lastname,$p->uNTRP);
                                echo "<td>$s</td>\n";
                                $cntrp_teama = $cntrp_teama + $team->team[$pos]->uNTRP;
                            } else {
                                echo "<td>??</td>\n";
                            }
                        }
                        echo "<td>" . $cntrp_teama . "</td>\n";
                        $cntrp_teamb = 0;
                        foreach (array('tbpa','tbpb') as $pos) {
                            if (array_key_exists($pos,$team->team)) {
                                $p =  $team->team[$pos];
                                $s = sprintf("%s %s (%3.2f)",$p->firstname,$p->lastname,$p->uNTRP);
                                echo "<td>$s</td>\n";
                                $cntrp_teamb = $cntrp_teamb + $team->team[$pos]->uNTRP;
                            } else {
                                echo "<td>??</td>\n";
                            }
                        }
                        echo "<td>" . $cntrp_teamb . "</td>\n";
                        $s = sprintf('%5.3f',abs($cntrp_teama-$cntrp_teamb));
                        echo "<td>$s</td>\n";
                    }
                    echo "</tr>\n";
                }
            }
        }
        echo "</table>\n";
    }
    
    // End the second row
    echo '</td></tr>';
    // And the top level table
    echo '</table>';
    
    echo "<br><br>";
    
    if (isset($_SESSION['season'])) {
        $season = $_SESSION['season'];
    } else {
        $season = "2012 Fall";
    }
    echo "<center><h2>";
    if ($season == "2012 Fall") {
        $season_text =  "Fall, 2012 ";
    } else {
        $season_text = $season;
    }

    $GLOBALS['TEMPLATE']['title'] = "<h3>Match Schedule for $season_text</h3>";
    $GLOBALS['TEMPLATE']['content'] = ob_get_clean();
    
    $GLOBALS['TEMPLATE']['extra_head'] = '<link rel="stylesheet" ' . 
        'type="text/css" href="css/members.css" title="Default"/>' .
        '<link rel="stylesheet" ' . 
        'type="text/css" href="css/members_cool.css" title="Cool"/>'
        ;
    
    include '../templates/template-page.php';
?>
