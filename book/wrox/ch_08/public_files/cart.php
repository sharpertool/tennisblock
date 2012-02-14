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

// empty the shopping cart and redirect user to list of categories
if (isset($_GET['empty']))
{
    $cart->removeAll();
    $_SESSION['cart'] = serialize($cart);
    header('Location: shop.php');
    end();
}

// item parameter indicates an attempt to add or remove items
if (isset($_GET['item']))
{
    // verify item is valid
    $query = sprintf('SELECT ITEM_ID FROM %sSHOP_INVENTORY WHERE ' . 
        'ITEM_ID = %d',
        DB_TBL_PREFIX,
        $_GET['item']);
    $result = mysql_query($query, $GLOBALS['DB']);

    if (mysql_num_rows($result))
    {
        $row = mysql_fetch_assoc($result);
        $item = $row['ITEM_ID'];
    
        // add item to cart
        if (isset($_GET['add']))
        {
            $cart->addItem($item);
        }

        // remove item from cart
        else if (isset($_GET['remove']))
        {
            $cart->removeItem($item);
        }
    }
    mysql_free_result($result);

    // save cart to session and redirect to the previously viewed page 
    $_SESSION['cart'] = serialize($cart);
    header('Location: ' . htmlspecialchars($_SERVER['HTTP_REFERER']));
    exit();
}

// view shopping cart's contents
else
{
    // update item quantities in shopping cart
    if (isset($_GET['update']))
    {
        foreach ($_POST['qty'] as $item => $qty)
        {
            $cart->addItem($item, $qty);
        }
    }

    ob_start();

    echo '<h1>Your Cart</h1>';
    echo '<p><a href="shop.php">Back to all categories</a>';

    // verify category parameter and construct suitable back link if passed
    if (isset($_GET['category']))
    {
        $query = sprintf('SELECT CATEGORY_ID, CATEGORY_NAME FROM ' .
            '%sSHOP_CATEGORY WHERE CATEGORY_ID = %d',
        DB_TBL_PREFIX,
        $_GET['category']);
        $result = mysql_query($query, $GLOBALS['DB']);

        if (mysql_num_rows($result))
        {
            $row = mysql_fetch_assoc($result);
            echo ' / <a href="shop.php?category=' . $row['CATEGORY_ID'] . 
                '">Back to ' . $row['CATEGORY_NAME'] . '</a>';
        }
        mysql_free_result($result);
    }
    echo '</p>';

    if ($cart->isEmpty)
    {
        echo '<p><b>Your cart is empty.</b></p>';
    }
    else
    {
        // display empty cart link 
        echo '<p><a href="cart.php?empty">';
        echo '<img src="img/cartempty.gif" alt="Empty Cart"/></a></p>';

        // encapsulate list in form so quantities may be changed
        echo '<form method="post" action="cart.php?update';
        // if a category was passed and was validated successfully earlier 
        // then append it to the action url so the back link remains available
        if  (isset($row['CATEGORY_ID']))
        {
            echo '&category=' . $row['CATEGORY_ID'];
        }
        echo '">';

        // list each item in the cart, keeping track of total price
        $total = 0;
        echo '<table>';
        echo '<tr><th>Item</th><th>Qty</th><th>Price</th><th>Total</th></tr>';
        foreach ($cart->contents as $id => $qty)
        {
            $query = sprintf('SELECT ITEM_NAME, PRICE FROM %sSHOP_INVENTORY ' .
                'WHERE ITEM_ID = %d',
                DB_TBL_PREFIX, 
                $id);
            $result = mysql_query($query, $GLOBALS['DB']);
    
            $row = mysql_fetch_assoc($result);
            echo '<tr>';
            echo '<td><a href="shop.php?item=' . $id . '">' . $row['ITEM_NAME'] .
                '</a></td>';
            echo '<td><select name="qty[' . $id . ']">';
            for ($i=0; $i < 11; $i++)
            {
                echo '<option ';
                if ($i == $qty)
                {
                    echo 'selected="selected" ';
                }
                echo 'value="' . $i . '">' . $i . '</option>';
            
            }
            echo '</td>';
            echo '<td>$' . number_format($row['PRICE'], 2) . '</td>';
            echo '<td>$' . number_format($row['PRICE'] * $qty, 2) . '</td>';
            echo '</tr>';
    
            $total += $row['PRICE'] * $qty;
            mysql_free_result($result);
        }
        echo '</table>';
        echo '<input type="submit" value="Update"/>';
        
        echo '<p>Total Items: ' . $cart->totalItems . '<br/>';
        echo 'Total Quantity: ' . $cart->totalQty . '</p>';
        echo '<p><b>Total Price: $' . number_format($total, 2) . '</b></p>';
    
        // display link to checkout
        echo '<p><a href="checkout.php">';
        echo '<img src="img/checkout.gif" alt="Proceed to Checkout"/></a></p>';
    }

    // save cart to session and display the page 
    $_SESSION['cart'] = serialize($cart);

    $GLOBALS['TEMPLATE']['content'] = ob_get_clean();
    include '../templates/template-page.php';
}
?>
