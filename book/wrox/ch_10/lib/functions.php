<?php
// return a string of random text of a desired length
function random_text($count, $rm_similar = true)
{
    $chars = array_flip(array_merge(range(0, 9), range('A', 'Z')));

    // remove similar looking characters
    if ($rm_similar)
    {
        unset($chars[0], $chars[1], $chars[2], $chars[5], $chars[8],
            $chars['B'], $chars['I'], $chars['O'], $chars['Q'],
            $chars['S'], $chars['U'], $chars['V'], $chars['Z']);
    }

    for ($i = 0; $i < $count; $i++)
    {
        $text .= array_rand($chars);
    }
    return $text;
}

// accept mm/dd/yy date string and convert to mysql format
function mysql_format_date($date)
{
    list($month, $day, $year) = explode('/', $date);
    return sprintf('%04d-%02d-%02d', $year, $month, $day);
}
?>
