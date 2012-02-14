<?php
    //include('checkLogin.php');
    //start the session
    session_start();
    if(!session_is_registered('username')){
        $logged_in = False;
    } else {
        $logged_in = True;
    }
?>
<html><head>

   <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
   <meta name="GENERATOR" content="Mozilla/4.04 [en] (WinNT; I) [Netscape]"><title>Friday Night Tennis Block</title>
   
</head>
<body>

<?php
// This is a test comment..
    if (isset($_SESSION['season'])) {
        $season = $_SESSION['season'];
    } else {
        $season = "Unknown Season";
    }
    echo "<center><h2>";
    if ($season == "2008 Fall") {
        echo "Fall, 2008 ";
    } elseif ($season == "2009 Fall") {
        echo "Fall, 2009 ";
    }
    echo "</h2></center>\n";
    echo "<center><h2>";
    echo "Friday Night Block";
    echo "</h2></center>\n";
?>        

<!-- Created with CoffeeCup Firestarter http://www.coffeecup.com -->

<table>
    <tr><td><a href="match_calendar.php" target="main">Match Calendar</a></td></tr>
    <tr><td><a href="member_list.php" target="main">Member List</a></td></tr>
    <tr><td><a href="member_availability.php" target="main">Member Availability</a></td></tr>
<?php
    if ($logged_in) {
        echo "<tr><td><a href=\"logout.php\" target=\"main\">Log Out</a></td></tr>\n";
    } else {
       echo "<tr><td><a href=\"login.php\" target=\"main\">Log In</a></td></tr>\n";
    }
?>
</table>

</body></html>
