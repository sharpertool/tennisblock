<?php 
// include shared code
include '../lib/common.php';
include '../lib/db.php';
include '../lib/functions.php';

// accept incoming search terms if the form has been submitted
$words = array();
if (isset($_GET['query']) && trim($_GET['query']))
{
    $words = explode_items($_GET['query'], ' ', false);

    // remove stop words from query
    $query = sprintf('SELECT TERM_VALUE FROM %sSEARCH_STOP_WORD',
        DB_TBL_PREFIX);
    $result = mysql_query($query, $GLOBALS['DB']);
    $stop_words = array();
    while ($row = mysql_fetch_assoc($result))
    {
        $stop_words[$row['TERM_VALUE']] = true;
    }
    mysql_free_result($result);

    $words_removed = array();
    foreach ($words as $index => $word)
    {
        if (isset($stop_words[strtolower($word)]))
        {
            $words_removed[] = $word;
            unset($words[$index]); 
        }
    }
}
// generate HTML form
ob_start();
?>
<form method="get"
 action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>">
 <div>
  <input type="text" name="query" id="query" value="<?php
   echo (count($words)) ? htmlspecialchars(join(' ', $words)) : '';?>"/>
  <input type="submit" value="Search"/>
 </div>
</form>
<?php

// begin processing query
if (count($words))
{
    // spell check the query words
    $spell_error = false;
    $suggest_words = array();
    $ps = pspell_new('en');
    foreach ($words as $index => $word)
    {
        if (!pspell_check($ps, $word))
        {
            if ($s = pspell_suggest($ps, $word))
            {
                if (strtolower($s[0]) != strtolower($word))
                {
                    // (ignore capitalization-related spelling errors)
                    $spell_error = true;
                    $suggest_words[$index] = $s[0];
                }
            }
        }
    }

    // formulate the search query using provided terms and submit it
    $join = '';
    $where = '';
    $query = 'SELECT DISTINCT D.DOCUMENT_URL, D.DOCUMENT_TITLE, ' .
        'D.DESCRIPTION FROM WROX_SEARCH_DOCUMENT D ';
    foreach ($words as $index => $word)
    {
        $join .= sprintf(
            'JOIN WROX_SEARCH_INDEX I%d ON D.DOCUMENT_ID = I%d.DOCUMENT_ID ' .
            'JOIN WROX_SEARCH_TERM T%d ON I%d.TERM_ID = T%d.TERM_ID ',
            $index, $index, $index, $index, $index);
    
        $where .= sprintf('T%d.TERM_VALUE = "%s" AND ', $index, 
            mysql_real_escape_string(strtolower($word), $GLOBALS['DB']));
    }
    $query .= $join . 'WHERE ' . $where;
    // trimmed 4 characters o remove trailing ' AND'
    $query = substr($query, 0, strlen($query) - 4);
    $result = mysql_query($query, $GLOBALS['DB']);

    // display results
    echo '<hr/>';
    $num_rows = mysql_num_rows($result);
    echo '<p>Search for <b>' . htmlspecialchars(join(' ', $words)) . 
        '</b> yielded ' . $num_rows . ' result' . 
        (($num_rows != 1) ? 's' : '') . ':</p>';

    // show suggested query if a possible misspelling was found
    if ($spell_error)
    {
        foreach ($words as $index => $word)
        {
            if (isset($suggest_words[$index]))
            {
                $words[$index] = $suggest_words[$index]; 
            }
        }
        echo '<p>Possible misspelling.  Did you mean <a href="' . 
            htmlspecialchars($_SERVER['PHP_SELF']) .'?query=' .
            urlencode(htmlspecialchars(join(' ', $words))) . '">' . 
            htmlspecialchars(join(' ', $words)) . '</a>?</p>';
    }

    echo '<ul>';
    while ($row = mysql_fetch_assoc($result))
    {
        echo '<li><b><a href="' . 
            htmlspecialchars($row['DOCUMENT_URL']) . '">' .
            htmlspecialchars($row['DOCUMENT_TITLE']) . '</a></b>- ' . 
            htmlspecialchars($row['DESCRIPTION']) . '<br/><i>' .
            htmlspecialchars($row['DOCUMENT_URL']) . '</i></li>';
    }
    echo '</ul>';
}
$GLOBALS['TEMPLATE']['content'] = ob_get_clean(); 

// display the page
include '../templates/template-page.php';
?>
