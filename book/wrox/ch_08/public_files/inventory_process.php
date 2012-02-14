<?php
include '../lib/common.php';
include '../lib/db.php';

// return HTML for category select list
if (isset($_GET['retrieve_category_select']))
{
    echo '<select id="cat_select" name="cat_select">';
    echo '<option>Select</option>';
    echo '<option value="new">Create New Category</option>';

    $query = sprintf('
        SELECT
            C.CATEGORY_ID, CATEGORY_NAME, COUNT(ITEM_ID) AS ITEM_COUNT
        FROM
            %sSHOP_CATEGORY C
                LEFT JOIN %sSHOP_INVENTORY I ON C.CATEGORY_ID = I.CATEGORY_ID
        GROUP BY
            C.CATEGORY_ID
        ORDER BY
            CATEGORY_NAME ASC',
        DB_TBL_PREFIX,
        DB_TBL_PREFIX);
    $result = mysql_query($query, $GLOBALS['DB']);

    while ($row = mysql_fetch_assoc($result))
    {
        printf('<option value="%d">%s &nbsp; (%s)</option>',
            $row['CATEGORY_ID'], $row['CATEGORY_NAME'], $row['ITEM_COUNT']); 
    }
    mysql_free_result($result);

    echo '</select>';
}

// return JSON-encoded string with category information
else if (isset($_GET['retrieve_category']))
{
    $query = sprintf('SELECT CATEGORY_NAME FROM %sSHOP_CATEGORY WHERE ' .
        'CATEGORY_ID = %d',
        DB_TBL_PREFIX,
        $_GET['id']);
    $result = mysql_query($query, $GLOBALS['DB']);

    $row = mysql_fetch_assoc($result);
    echo json_encode(array('cat_name' => $row['CATEGORY_NAME']));

    mysql_free_result($result);
}

// process save request for category information
else if (isset($_GET['save_category']))
{
    // create a new record
    if ($_POST['id'] == 'new')
    {
        $query = sprintf('INSERT INTO %sSHOP_CATEGORY (CATEGORY_NAME) ' .
            'VALUES ("%s")',
            DB_TBL_PREFIX,
            mysql_real_escape_string($_POST['name'], $GLOBALS['DB']));
    }
    else
    {
        // delete an existing record
        if (isset($_POST['delete']))
        {
            $query = sprintf('DELETE FROM %sSHOP_CATEGORY WHERE ' . 
                'CATEGORY_ID = %d',
                DB_TBL_PREFIX,
                $_POST['id']);
        }
        // update an existing record
        else
        {
            $query = sprintf('UPDATE %sSHOP_CATEGORY SET ' . 
                'CATEGORY_NAME = "%s" WHERE CATEGORY_ID = %d',
                DB_TBL_PREFIX,
                mysql_real_escape_string($_POST['name'], $GLOBALS['DB']),
                $_POST['id']);
        }
    }
    mysql_query($query, $GLOBALS['DB']);
}

// return HTML for item select list
else if (isset($_GET['retrieve_item_select']))
{
    echo '<select id="item_select" name="item_select">';
    echo '<option>Select</option>';
    echo '<option value="new">Create New Item</option>';

    $query = sprintf('SELECT ITEM_ID, ITEM_NAME FROM %sSHOP_INVENTORY ' .
        'WHERE CATEGORY_ID = %d ORDER BY ITEM_NAME ASC',
        DB_TBL_PREFIX,
        $_GET['id']);
    $result = mysql_query($query, $GLOBALS['DB']);

    while ($row = mysql_fetch_assoc($result))
    {
        echo '<option value="' . $row['ITEM_ID'] . '">' . $row['ITEM_NAME'] . 
            '</option>'; 
    }
    mysql_free_result($result);

    echo '</select>';
}

// return JSON-encoded string with item information
else if (isset($_GET['retrieve_item']))
{
    $query = sprintf('SELECT ITEM_NAME, ITEM_DESCRIPTION, PRICE, ' . 
        'ITEM_IMAGE FROM %sSHOP_INVENTORY WHERE ITEM_ID = %d',
        DB_TBL_PREFIX,
        $_GET['id']);
    $result = mysql_query($query, $GLOBALS['DB']);

    $row = mysql_fetch_assoc($result);
    echo json_encode(array(
        'item_name' => $row['ITEM_NAME'],
        'item_description' => $row['ITEM_DESCRIPTION'],
        'item_price' => $row['PRICE'],
        'item_image' => $row['ITEM_IMAGE']));

    mysql_free_result($result);
}

// process save request for item information
else if (isset($_GET['save_item']))
{
    // create a new record
    if ($_POST['id'] == 'new')
    {
        $query = sprintf('INSERT INTO %sSHOP_INVENTORY (ITEM_NAME, ' . 
            'ITEM_DESCRIPTION, PRICE, ITEM_IMAGE, CATEGORY_ID) VALUES ' . 
            '("%s", "%s", %02f, %d)',
            DB_TBL_PREFIX,
            mysql_real_escape_string($_POST['name'], $GLOBALS['DB']),
            mysql_real_escape_string($_POST['description'], $GLOBALS['DB']),
            $_POST['price'],
            mysql_real_escape_string($_POST['image'], $GLOBALS['DB']),
            $_POST['cat_id']);
    }
    else
    {
        // delete an existing record
        if (isset($_POST['delete']))
        {
            $query = sprintf('DELETE FROM %sSHOP_INVENTORY WHERE ' . 
                'ITEM_ID = %d',
                DB_TBL_PREFIX,
                $_POST['id']);
        }
        // update an existing record
        else
        {
            $query = sprintf('UPDATE %sSHOP_INVENTORY SET ' . 
                'ITEM_NAME = "%s", ITEM_DESCRIPTION = "%s", ' . 
                'PRICE = %02d, ITEM_IMAGE = "%s", CATEGORY_ID = %d ' .
                'WHERE ITEM_ID = %d',
                DB_TBL_PREFIX,
                mysql_real_escape_string($_POST['name'], $GLOBALS['DB']),
                mysql_real_escape_string($_POST['description'], $GLOBALS['DB']),
                $_POST['price'],
                mysql_real_escape_string($_POST['image'], $GLOBALS['DB']),
                $_POST['cat_id'],
                $_POST['id']);
        }
    }
    mysql_query($query, $GLOBALS['DB']);
}
?>
