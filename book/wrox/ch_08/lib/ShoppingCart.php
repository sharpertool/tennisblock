<?php
class ShoppingCart
{
    // collection of items placed in the shopping cart
    private $items;

    // initialize a ShoppingCart object
    public function __construct()
    {
        $this->items = array();
    }

    // expose read-only convenience properties
    public function __get($value)
    {
        switch ($value)
        {
            // contents - returns the entire contents of the cart
            case 'contents':
                return $this->items;
                brake;
    
            // isEmpty - returns whether or not the cart is empty
            case 'isEmpty':
                return (count($this->items) == 0);
                break;
    
            // totalItems - returns the total number of distinct items
            // in the cart
            case 'totalItems':
                return count($this->items);
                break;
    
            // totalQty - returns the total quantity of items in the cart
            case 'totalQty':
                return array_sum($this->items);
                break;
         }
    }

    // add an item to the shopping cart    
    public function addItem($item, $qty = 1)
    {
        if (!$qty)
        {
            $this->removeItem($item);
        }
        else
        {
            $this->items[$item] = $qty;
        }
    }

    // returns an item's quantity in the cart 
    public function qtyItem($item)
    {
        if (!isset($this->items[$item]))
        {
            return 0;
        }
        else
        {
            return $this->items[$item];
        }
    }

    // empty the contents of the shopping cart
    public function removeAll()
    {
        $this->items = array();
    }

    // remove an item from the shopping cart
    public function removeItem($item)
    {
        unset($this->items[$item]);
    }
}
?>
