<?php
// convert a list of items (separated by newlines by default) into an array
// omitting blank lines and optionally duplicates
function explode_items($text, $separator = "\n", $preserve = true)
{
    $items = array();
    foreach (explode($separator, $text) as $value)
    {
        $tmp = trim($value);
        if ($preserve)
        {
             $items[] = $tmp;
        }
        else
        {
            if (!empty($tmp))
            {
                $items[$tmp] = true;
            }
        }
    }

    if ($preserve)
    {
        return $items;
    }
    else
    {
        return array_keys($items);
    }
}
?>
