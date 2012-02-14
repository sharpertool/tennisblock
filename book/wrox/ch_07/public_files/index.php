<?php
// include shared code
include '../lib/config.php';

// accept incoming parameters
$album = (isset($_GET['album'])) ? $_GET['album'] : '';
$album_p = BASEDIR . '/' . $album;

$file = (isset($_GET['file'])) ? $_GET['file'] : '';
$file_p = $album_p . '/' . $file;

// generate image view
if ($album && $file)
{
    // redirect to album list if album or file is outside allowed base
    // directory or does not exist
    if (strpos(realpath($album_p), BASEDIR) !== 0 ||
        strpos(realpath($file_p), BASEDIR) !== 0 || !file_exists($file_p))
    {
        header('Location: ' . htmlspecialchars($_SERVER['PHP_SELF']));
        exit();
    }
    ob_start();

    // provide link for album view
    echo '<p><a href="' . htmlspecialchars($_SERVER['PHP_SELF']) . '?album='.
        urlencode($album) . '">&lt; Back to ' . htmlspecialchars($album) .
        '</a></p>';

    switch (substr($file, strrpos($file, '.') + 1))
    {
        // jpeg files are included using the img element
        case 'jpg':
        case 'jpeg':
            echo '<img src="view.php?file=' . urlencode($album . '/' . 
                $file) . '" alt="' . htmlspecialchars($file) . '"/>';
            break;

        // QuickTime files are included using the object/embed elements
        case 'mov':
            echo '<object type="video/quicktime" data="view.php?file=' .
                urlencode($album . '/' . $file) . '">';
            echo '<param name="movie" value="view.php?file=' .
                urlencode($album . '/' . $file) . '"/>';
            echo '<embed type="video/quicktime" src="view.php?file=' .
                urlencode($album . '/' . $file) . '"/>';
            echo '</object>';
 
            break;
        // redirect if file format is not valid
        default:
            header('Location: ' . htmlspecialchars($_SERVER['PHP_SELF']));
            exit();       
    }

    $GLOBALS['TEMPLATE']['content'] = ob_get_contents();
    ob_end_clean();
}

// generate album view
else if ($album)
{
    // redirect to album list if album does not exist or is outside the
    // allowed base directory
    if (strpos(realpath($album_p), BASEDIR) !== 0 || !file_exists($album_p))
    {
        header('Location: ' . htmlspecialchars($_SERVER['PHP_SELF']));
        exit();       
    }
    ob_start();

    // provide link for album index
    echo '<p><a href="' . htmlspecialchars($_SERVER['PHP_SELF']) . '">' .
        '&lt; Back to album index</a></p>';

    // retrieve album description if available
    if (file_exists($album_p . '/desc.txt'))
    {
        echo '<p>' . nl2br(file_get_contents($album_p . '/desc.txt')) . '</p>';
    }

    // read in list of image and QuickTime files
    $dir = opendir($album_p);
    $images = array();
    while($f = basename(readdir($dir)))
    {
        if($f == '.' || $f == '..') continue;

        if (!is_dir($f))
        {
            $ext = (substr($f, strpos($f, '.') + 1));
            if ($ext == 'jpg' || $ext == 'jpeg' || $ext == 'mov')
            {
                $images[] = $f;
            }
        }
    }
    closedir($dir);

    // sort images
    natcasesort($images);

    //display thumbnails in a table
    $counter = 0;
    $columns = 7;
    echo '<table border="1">';
    foreach ($images as $image)
    {
        if (0 == ($counter % $columns))
        {
            echo '<tr>';
        }
        echo '<td style="width: '. (100 / $columns) . '%; ';
        echo 'vertical-align: top; padding: 10px; text-align: center;">';

        printf ('<a href="%s?album=%s&file=%s"><img src="thumbnail.php?' .
            'file=%s" alt="%s"/></a> ',
            htmlspecialchars($_SERVER['PHP_SELF']),
            urlencode($album),
            urlencode($image),
            urlencode($album . '/' . $image),
            htmlspecialchars($image));

        echo '</td>';
        if (0 == (++$counter % $columns))
        {
            echo '</tr>';
        }
    }
    // finish table's row with blank cells if necessary
    while ($counter++ % $columns)
    {
        echo '<td>&nbsp;</td>';
    }
    if (substr(ob_get_contents(), -5) == '</td>')
    {
        echo '</tr>';
    }
    echo '</table>';

    $GLOBALS['TEMPLATE']['content'] = ob_get_contents();
    ob_end_clean();
}

// generate default view showing list of available albums
else
{
    ob_start();

    // retrieve list of albums
    $albums = array();
    $dir = opendir(BASEDIR);
    while($f = basename(readdir($dir)))
    {
        if($f == '.' || $f == '..') continue;
        
        if (is_dir(BASEDIR . '/' . $f))
        {
            $albums[] = $f;
        }
    }
    closedir($dir);

    // sort albums
    natcasesort($albums);

    // display album list
    echo '<p>Albums</p>';
    echo '<ul>';
    foreach ($albums as $album)
    {
        printf('<li><a href="%s?album=%s">%s</a></li>',
        htmlspecialchars($_SERVER['PHP_SELF']),
        urlencode($album),
        htmlspecialchars($album));
    }
    echo '</ul>';

    $GLOBALS['TEMPLATE']['content'] = ob_get_contents();
    ob_end_clean();
}


/*// include shared code
include '../lib/config.php';

// accept incoming parameters
$album = (isset($_GET['album'])) ? $_GET['album'] : '';
$album_p = BASEDIR . '/' . $album;

$file = (isset($_GET['file'])) ? $_GET['file'] : '';
$file_p = $album_p . '/' . $file;

// generate image view
if ($album && $file)
{
    // redirect to album list if album or file is outside allowed base
    // directory or does not exist
    if (strpos(realpath($album_p), BASEDIR) !== 0 ||
        strpos(realpath($file_p), BASEDIR) !== 0 || !file_exists($file_p))
    {
//        header('Location: ' . htmlspecialchars($_SERVER['PHP_SELF']));
//        exit();
echo $file_p;       
    }
    ob_start();

    // provide link for album view
    echo '<p><a href="' . htmlspecialchars($_SERVER['PHP_SELF']) . '?album='.
        urlencode($album) . '">&lt; Back to ' . htmlspecialchars($album) .
        '</a></p>';

    switch (substr($file, strrpos($file, '.') + 1))
    {
        // jpeg files are included using the img element
        case 'jpg':
        case 'jpeg':
            echo '<img src="view.php?file=' . urlencode($album . '/' . 
                $file) . '" alt="' . htmlspecialchars($file) . '"/>';
            break;

        // quicktime files are included using the object/embed elements
        case 'mov':
            echo '<object type="video/quicktime" data="view.php?file=' .
                urlencode($album . '/' . $file) . '">';
            echo '<param name="movie" value="view.php?file=' .
                urlencode($album . '/' . $file) . '"/>';
            echo '<embed type="video/quicktime" src="view.php?file=' .
                urlencode($album . '/' . $file) . '"/>';
            echo '</object>';
 
            break;
        // redirect if file format is not valid
        default:
            header('Location: ' . htmlspecialchars($_SERVER['PHP_SELF']));
            exit();       
    }

    $GLOBALS['TEMPLATE']['content'] = ob_get_contents();
    ob_end_clean();
}

// generate album view
else if ($album)
{
    // redirect to album list if album does not exist or is outside the
    // allowed base directory
    if (strpos(realpath($album_p), BASEDIR) !== 0 || !file_exists($album_p))
    {
        header('Location: ' . htmlspecialchars($_SERVER['PHP_SELF']));
        exit();       
    }
    ob_start();

    // provide link for album index
    echo '<p><a href="' . htmlspecialchars($_SERVER['PHP_SELF']) . '">' .
        '&lt; Back to album index</a></p>';

    // retrieve album description if available
    if (file_exists($album_p . '/desc.txt'))
    {
        echo '<p>' . nl2br(file_get_contents($album_p . '/desc.txt')) . '</p>';
    }

    // read in list of images
    $dir = opendir($album_p);
    $images = array();
    while($f = basename(readdir($dir)))
    {
        if($f == '.' || $f == '..') continue;

        if (!is_dir($f))
        {
            $images[] = $f;
        }
    }
    closedir($dir);

    // sort images
    natcasesort($images);

    //gather thumbnails
    foreach ($images as $image)
    {
        switch (substr($image, strpos($image, '.') + 1))
        {
            case 'jpg':
            case 'jpeg':
            case 'mov':
                printf ('<a href="%s?album=%s&file=%s"><img ' . 
                    'src="thumbnail.php?file=%s" alt="%s"/></a> ',
                    htmlspecialchars($_SERVER['PHP_SELF']),
                    urlencode($album),
                    urlencode($image),
                    urlencode($album . '/' . $image),
                    htmlspecialchars($image));
                break;
        }
    }

    $GLOBALS['TEMPLATE']['content'] = ob_get_contents();
    ob_end_clean();
}

// generate default view showing list of available albums
else
{
    ob_start();

    // retrieve list of albums
    $albums = array();
    $dir = opendir(BASEDIR);
    while($f = basename(readdir($dir)))
    {
        if($f == '.' || $f == '..') continue;
        
        if (is_dir(BASEDIR . '/' . $f))
        {
            $albums[] = $f;
        }
    }
    closedir($dir);

    // sort albums
    natcasesort($albums);

    // display album list
    echo '<p>Albums</p>';
    echo '<ul>';
    foreach ($albums as $album)
    {
        printf('<li><a href="%s?album=%s">%s</a></li>',
        htmlspecialchars($_SERVER['PHP_SELF']),
        urlencode($album),
        htmlspecialchars($album));
    }
    echo '</ul>';

    $GLOBALS['TEMPLATE']['content'] = ob_get_contents();
    ob_end_clean();
}

// display the page
*/// include '../templates/template-page.php';
echo $GLOBALS['TEMPLATE']['content'];
?>
