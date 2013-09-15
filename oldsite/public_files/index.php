<?php
    //include('checkLogin.php');
    //start the session
    session_start();
    if(!session_is_registered('username')){
        $logged_in = False;
    } else {
        $logged_in = True;
    }

	include_once 'inc/dbconninfo.php';
?>
<html>
<head>
	<meta http-equiv="X-UA-Compatible" content="IE=7,IE=9,chrome=IE8">
	<title>Friday Night Tennis Block</title>

	<link rel="stylesheet" href="/css/reset.css" type="text/css" media="screen" />
	<link rel="stylesheet" href="/css/smoothness/jquery-ui-1.8.23.custom.css" type="text/css" media="screen" />
	<link rel="stylesheet" href="/css/layout.css" type="text/css" media="screen" />
	<link rel="stylesheet" href="/css/main.css" type="text/css" media="screen" />
	<link rel="stylesheet" href="/css/forms.css" type="text/css" media="screen" />

	<script type="text/javascript">

		// Avoid issues in IE* where console is not defined!
		if (!window.console) {
			window.console = {};
			window.console.log = function() {};
		}

	</script>

</head>
<body>

	<div id="top_bar">
		<div id="projectBar" class="shadow">
			<div id="logo_header">
				<img src="/img/toolbar_logo.png" width="100" height="16" alt="Tennis block"/>
			</div>

			<div class="projectbar_button" id="help_button">
				Help
			</div>

			<div class="projectbar_button" id="login">
				Login
			</div>

		</div>
		<div id="tabs">
			<ul>
				<li id="menu_home">Home</li>
				<li id="menu_calendar">Match Calendar</li>
				<li id="menu_members">Member List</li>
				<li id="menu_availability">Member Availability</li>
			</ul>
		</div>

	</div>

	<div id="content">
		<div id="home">

		</div>

		<div id="calendar">

		</div>

		<div id="members">

		</div>


		<div id="availability">

		</div>

	</div>

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
	?>

	<script type="text/javascript" src="/js/library/jquery-1.8.0.min.js"></script>
	<script type="text/javascript" src="/js/library/jquery-ui-1.8.23.custom.min.js"></script>
	<script type="text/javascript" src="/js/library/jquery.corner.js"></script>
	<script type="text/javascript" src="/js/library/jquery.layout.min-1.2.0.js"></script>
	<script type="text/javascript" src="/js/library/underscore.js"></script>

	<script type="text/javascript" src="/js/library/splitter.js"></script>
	<script type="text/javascript" src="/js/library/jquery.imgpreload.min.js"></script>

	<script type="text/javascript" src="/js/library/jquery.dataTables.min.js"></script>
	<script type="text/javascript" src="/js/library/jquery.jeditable.js"></script>
	<script type="text/javascript" src="/js/library/jquery.dataTables.editable.js"></script>

	<script type="text/javascript" src="/js/library/json2.js"></script>
	<script type="text/javascript" src="/js/library/jquery.cookie.js"></script>
	<script type="text/javascript" src="/js/library/log4javascript_uncompressed.js"></script>
	<script type="text/javascript" src="/js/library/loggr.min.js"></script>
	<script type="text/javascript" src="/js/tennisblock.js"></script>
	<script type="text/javascript" src="/js/main.js"></script>
	<script type="text/javascript">

		if (location.host.search('tennisblock.local') >= 0) {
			tblk_runEnv = 'test';
			tblk_dbhost='bondinorth.local';
		} else if (location.host.search('tennisblock.net') >= 0) {
			tblk_runEnv = 'prod';
			tblk_dbhost='localhost';
		}

	</script>

</body>
</html>
