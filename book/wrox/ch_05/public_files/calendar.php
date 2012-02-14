<?php
include '../lib/common.php';
include '../lib/db.php';

// view definitions
define('DAY_HR_START', 9);
define('DAY_HR_END', 17);

// accept incoming URL parameter
$timestamp = (isset($_GET['t'])) ? $_GET['t'] : time();

// determine useful aspects of the requested month
list($month, $day, $year) = explode('/', date('m/d/Y', $timestamp));
$first_day_of_month = date('w', mktime(0, 0, 0, $month, 1, $year));
$total_days = date('t', $timestamp);

// add new event
if (isset($_POST['submitted']))
{
    // validate incoming values
    $evt_name = (isset($_POST['evt_name'])) ? $_POST['evt_name'] : '';
    $evt_name = trim($evt_name);
    if (!$evt_name)
    {
        $evt_name = 'Unknown';
    }
    $evt_pm = (isset($_POST['evt_pm']) && $_POST['evt_pm'] == 'yes');
    $evt_hour = (isset($_POST['evt_hour'])) ? (int)$_POST['evt_hour'] : 0;
    if ($evt_pm)
    {
        $evt_hour += 12;
    }
    if ($evt_hour == 24)
    {
       $evt_hour = 12;
    }
    else if ($evt_hour == 12)
    {
       $evt_hour = 0;
    }
    $evt_min = (isset($_POST['evt_min'])) ? (int)$_POST['evt_min'] : 0;
    $evt_notify = (isset($_POST['evt_notify']) &&
        $_POST['evt_notify'] == 'yes');

    // add to database
    $query = sprintf('INSERT INTO %sCALENDAR (EVENT_NAME, EVENT_TSTAMP, ' . 
        'NOTIFY) VALUES ("%s", "%04d-%02d-%02d %02d:%02d:00", %d)',
        DB_TBL_PREFIX,
        mysql_real_escape_string($evt_name, $GLOBALS['DB']),
        $year, $month, $day,
        $evt_hour, $evt_min,
        $evt_notify);
    mysql_query($query, $GLOBALS['DB']);
}

// output table header
ob_start();
echo '<table id="day_calendar">';
echo '<tr id="day_calendar_header"><th colspan="2">';
echo '<a href="'. htmlspecialchars($_SERVER['PHP_SELF']) . '?t=' .
    strtotime('-1 day', $timestamp) . '">&lt;</a> &nbsp;';
echo date('l F d, Y', $timestamp);
echo '&nbsp; <a href="'. htmlspecialchars($_SERVER['PHP_SELF']) . '?t=' .
    strtotime('+1 day', $timestamp) . '">&gt;</a>';
echo '</th></tr>';

// output cells
for ($i = DAY_HR_START; $i <= DAY_HR_END; $i++)
{
    for ($j = 0; $j < 60; $j += 15)
    {
        echo '<tr>';

        if ($i < 12)
        {
            printf('<td class="time">%d:%02d %s</td>', $i, $j, 'AM');
        }
        else if ($i > 12)
        {
            printf('<td class="time">%d:%02d %s</td>', $i - 12,
                $j, 'PM');
        }
        else
        {
            printf('<td class="time">%d:%02d %s</td>', $i, $j, 'PM');
        }
        echo '<td class="event">';

        $query = sprintf('SELECT EVENT_NAME FROM %sCALENDAR WHERE ' .
            'EVENT_TSTAMP = "%04d-%02d-%02d %02d:%02d:00"',
            DB_TBL_PREFIX,
            $year, $month, $day,
            $i, $j);
        $result = mysql_query($query, $GLOBALS['DB']);

        if (mysql_num_rows($result))
        {
            while ($row = mysql_fetch_assoc($result))
            {
                echo '<div>' . htmlspecialchars($row['EVENT_NAME']) .
                    '</div>';
            }
        }
        else
        {
            echo '&nbsp;';
        }
        mysql_free_result($result);
        echo '</td>';
        echo '</tr>';
    }
}
echo '</table>';

// display month calendar
echo '<table id="calendar">';
echo '<tr id="calendar_header"><th colspan="7">';
echo '<a href="' . htmlspecialchars($_SERVER['PHP_SELF']) . '?t=' .
    strtotime('-1 month', $timestamp) . '">&lt;</a> &nbsp;';
echo date('F', $timestamp) . ' ' . $year;
echo '&nbsp; <a href="' . htmlspecialchars($_SERVER['PHP_SELF']) . '?t=' .
    strtotime('+1 month', $timestamp) . '">&gt;</a>';
echo '</th></tr>';
echo '<tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th>' .
    '<th>Fri</th><th>Sat</th></tr>';
$current = 1;
while ($current <= $total_days)
{
    echo '<tr class="calendar_dates">';
    for ($i = 0; $i < 7; $i++)
    {
        if (($current == 1 && $i < $first_day_of_month) ||
            ($current > $total_days))
        {
            echo '<td class="empty">&nbsp</td>';
            continue;
        }
        echo '<td><a href="' . htmlspecialchars($_SERVER['PHP_SELF']) .
            '?t=' . mktime(0, 0, 0, $month, $current, $year) . '">' .
            $current . '</a></td>';
        $current++;
    }
    echo '</tr>';
}
echo '</table>';

// Form to add event
?>
<h2>Add Event</h2>
<form action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']) . '?t=' . 
 $timestamp; ?>" method="post">
 <table>
  <tr>
   <td class="label"><label for="evt_name">Event:</label></td>
   <td><input type="text" id="evt_name" name="evt_name"></td>
  </tr><tr>
   <td class="label"><label for="evt_hour">Time:</label></td>
   <td>
    <select name="evt_hour" id="evt_hour">
     <option value="12">12</option>
<?php

    for ($i = 1; $i < 12; $i++)
    {
        printf('<option value="%d">%02d</option>', $i, $i);
    }
?>
    </select> : <select name="evt_min">
<?php
    for ($i = 0; $i < 59; $i += 15)
    {
            printf('<option value="%d">%02d</option>', $i, $i);
    }
?>
    </select>
    <select name="evt_pm">
     <option value="no">AM</option>
     <option value="yes">PM</option>
    </select>
   </td>
  </tr><tr>
   <td class="label">Notify</td>
   <td>
    <input type="radio" name="evt_notify" id="evt_notify_yes" value="yes" 
     checked="checked"/>
    <label for="evt_notify_yes">Yes</label>
    <input type="radio" name="evt_notify" id="evt_notify_no" value="no" />
    <label for="evt_notify_no">No</label>
   </td>
  </tr><tr>
   <td></td>
   <td>
    <input type="hidden" name="submitted" value="true"/>
    <input type="submit" value="Add Event"/></td>
  </tr>
 </table>
</form>

<h2>Also Scheduled</h2>
<?php
// retrieve and display events that fall outside the daily-view hours
$query = sprintf('SELECT EVENT_NAME, UNIX_TIMESTAMP(EVENT_TSTAMP) AS ' .
    'EVENT_TSTAMP FROM %sCALENDAR WHERE EVENT_TSTAMP NOT BETWEEN ' . 
    '"%4d-%02d-%02d %02d:00:00" AND "%4d-%02d-%02d %02d:59:59" ORDER BY ' .
    'EVENT_TSTAMP ASC, EVENT_NAME ASC',
     DB_TBL_PREFIX,
     $year, $month, $day, DAY_HR_START,
     $year, $month, $day, DAY_HR_END);
$result = mysql_query($query, $GLOBALS['DB']);

echo '<ul>';
if (mysql_num_rows($result))
{
    while ($row = mysql_fetch_assoc($result))
    {
        echo '<li>' . date('h:i A - ', $row['EVENT_TSTAMP']) .
        htmlspecialchars($row['EVENT_NAME']) . '</li>';
    }
}
else
{
    echo '<p><i>No other events scheduled</i></p>';
}
mysql_free_result($result);
echo '</ul>';

// link to download iCal file
echo '<p><a href="export.php">Export as iCalendar file</a></p>';


$GLOBALS['TEMPLATE']['content'] = ob_get_clean();

$GLOBALS['TEMPLATE']['extra_head'] = '<link rel="stylesheet" ' . 
    'type="text/css" href="css/calendar.css"/>';

include '../templates/template-page.php';
?>
