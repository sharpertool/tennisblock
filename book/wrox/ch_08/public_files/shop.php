<?php
include '../lib/common.php';
include '../lib/db.php';
include '../lib/ShoppingCart.php';

// create or resume session and retrieve shopping cart
session_start();
if (isset($_SESSION['cart']))
{
    $cart = unserialize($_SESSION['cart']);
}
else
{
    $cart = new ShoppingCart(); 
}

// display sales page for a particular item
if (isset($_GET['item']))
{
    // verify item exists
    $query = sprintf('
        SELECT
            ITEM_ID, ITEM_NAME, ITEM_DESCRIPTION, PRICE, ITEM_IMAGE,
            C.CATEGORY_ID, CATEGORY_NAME
        FROM
           %sSHOP_INVENTORY I
               JOIN %sSHOP_CATEGORY C ON I.CATEGORY_ID = C.CATEGORY_ID
        WHERE
            ITEM_ID = %d',
        DB_TBL_PREFIX,
        DB_TBL_PREFIX,
        $_GET['item']);
    $result = mysql_query($query, $GLOBALS['DB']);

    // item does not exist so redirect to main categories list
    if (!mysql_num_rows($result))
    {
        mysql_free_result($result);
        header('Location: shop.php');
        exit();
    }

    $row = mysql_fetch_assoc($result);

    ob_start();
    echo '<p><a href="cart.php?category=' . $row['CATEGORY_ID'] . '">'; 
    echo '<img src="img/cartview.gif" alt="View Cart"/></a></p>';

    echo '<h1>' . $row['ITEM_NAME'] . '</h1>';

    echo '<p><a href="shop.php">Back to all categories</a> / ';
    echo '<a href="shop.php?category=' . $row['CATEGORY_ID']. '">Back to ' . 
        $row['CATEGORY_NAME'] . '</a></p>'; 

    echo '<table>';
    echo '<tr><td rowspan="3">';
    echo '<img src="' . $row['ITEM_IMAGE'] . '"/></td>';
    echo '<td><b>' . $row['ITEM_NAME'] . '</b></td></tr>';
    echo '<tr><td>' . nl2br($row['ITEM_DESCRIPTION']) . '</td></tr>';
    echo '<tr><td>$' . number_format($row['PRICE'], 2) . '<br/>';

    // show link to either add or remove item from cart
    if (!$cart->qtyItem($row['ITEM_ID']))
    {
        echo '<a href="cart.php?add&item=' . $row['ITEM_ID'] . '">';
        echo '<img src="img/cartadd.gif" alt="Add to Cart"/></a>';
    }
    else
    {
        echo '<a href="cart.php?remove&item=' . $row['ITEM_ID'] . '">';
        echo '<img src="img/cartremove.gif" alt="Remove from Cart"/></a>';
    }
    echo '</td></tr>';
    echo '</table>';

    $GLOBALS['TEMPLATE']['content'] = ob_get_clean();
}

// display list of items in category
else if (isset($_GET['category']))
{
    // verify if category parameter is valid
    $query = sprintf('SELECT CATEGORY_ID, CATEGORY_NAME FROM ' .
        '%sSHOP_CATEGORY WHERE CATEGORY_ID = %d',
        DB_TBL_PREFIX,
        $_GET['category']);
    $result = mysql_query($query, $GLOBALS['DB']);

    // category does not exist so redirect to main categories list
    if (!mysql_num_rows($result))
    {
        mysql_free_result($result);
        header('Location: shop.php');
        exit();
    }

    $row = mysql_fetch_assoc($result);
    $id = $row['CATEGORY_ID'];
    $name = $row['CATEGORY_NAME'];
    mysql_free_result($result);

    ob_start();
    echo '<p><a href="cart.php?category=' . $id . '">';
    echo '<img src="img/cartview.gif" alt="View Cart"/></a></p>';

    echo '<h1>Products in ' . $name . '</h1>';

    echo '<p><a href="shop.php">Back to all categories</a></p>';

    // retrieve items
    $query = sprintf('SELECT ITEM_ID, ITEM_NAME, ITEM_IMAGE ' . 
        'FROM %sSHOP_INVENTORY WHERE CATEGORY_ID = %d ORDER BY ITEM_NAME ASC',
        DB_TBL_PREFIX,
        $id);
    $result = mysql_query($query, $GLOBALS['DB']);

    while ($row = mysql_fetch_assoc($result))
    {
        echo '<table>';
        echo '<tr><td><img src="' . $row['ITEM_IMAGE'] . 
            '" style="width:50px;height:50px;"/></td>';
        echo '<td><a href="shop.php?item=' . $row['ITEM_ID'] . '">' .
            $row['ITEM_NAME'] . '</a>' . '</td></tr>';
        echo '</table>';
    }

    $GLOBALS['TEMPLATE']['content'] = ob_get_clean();
}

// display main list of categories and the number of products within each
else
{
    ob_start();
    echo '<p><a href="cart.php">' . 
        '<img src="img/cartview.gif" alt="View Cart"/></a></p>';

    echo '<h1>All Categories</h1>';

    // Note: LEFT JOIN not specified so any categories without products will
    // not be included in the results
    $query = sprintf('
        SELECT
            C.CATEGORY_ID, CATEGORY_NAME, COUNT(ITEM_ID) AS ITEM_COUNT
        FROM
            %sSHOP_CATEGORY C
                JOIN %sSHOP_INVENTORY I ON C.CATEGORY_ID = I.CATEGORY_ID
        GROUP BY
            C.CATEGORY_ID
        ORDER BY
            CATEGORY_NAME ASC',
        DB_TBL_PREFIX,
        DB_TBL_PREFIX);
    $result = mysql_query($query, $GLOBALS['DB']);

    echo '<ul>';
    while ($row = mysql_fetch_assoc($result))
    {
        printf('<li><a href="shop.php?category=%d">%s</a> (%d %s)</li>',
            $row['CATEGORY_ID'],
            $row['CATEGORY_NAME'], 
            $row['ITEM_COUNT'],
            (($row['ITEM_COUNT'] == 1) ? 'product' : 'products'));
    }
    mysql_free_result($result);
    echo '</ul>';

    $GLOBALS['TEMPLATE']['content'] = ob_get_clean();
}

// display the page
include '../templates/template-page.php';
?>
