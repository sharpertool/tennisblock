#! /usr/bin/php
<?php
include '../lib/common.php';
include '../lib/db.php';

// retrieve list of tables
$table_result = mysql_query('SHOW TABLES', $GLOBALS['DB']);
while ($table_row = mysql_fetch_array($table_result))
{
    // retrieve list of column names in table 
    $column_result = mysql_query('SHOW COLUMNS FROM ' . $table_row[0],
        $GLOBALS['DB']);    
    while ($column_row = mysql_fetch_assoc($column_result))
    {
        // if the table has an IS_DELETED field then delete old records
        if ($column_row['Field'] == 'IS_DELETED')
        {
            mysql_query('DELETE FROM ' . $table_row[0] . ' WHERE ' .
                'IS_DELETED = 1', $GLOBALS['DB']);

            // break out to process next table
            mysql_free_result($column_result);
            break;
        }
    }
    mysql_free_result($column_result);
}
mysql_free_result($table_result);
mysql_close($GLOBALS['DB']);
?>

