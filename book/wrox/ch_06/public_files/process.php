<?php
include '../lib/common.php';
include '../lib/config.php';

// see http://us2.php.net/manual/en/function.filesize.php#77518
function size_human_read ($size)
{
    // Only format B through GB. If someone can afford the bandwidth to
    // transfer files >= TB then he can afford to pay me to patch this
    // code if beyond that is required! :)
    $sizes = array('B', 'KB', 'MB', 'GB');

    $prev_s = end($sizes);
    foreach ($sizes as $s)
    {
        if ($size < 1024)
        {
            break;
        }
        if ($s != $prev_s)
        {
            $size /= 1024;
        }
    }
    if ($s == $sizes[0])
    {
        return sprintf('%01d %s', $size, $s);
    }
    else
    {
        return sprintf('%01.2f %s', $size, $s);
    }
}

// return HTML row for file display
function directory_row($file, $show_stats = true)
{
    // get information for $file
    $is_dir = is_dir($file);
    $info = stat($file);

    // keep track of row count to alternating odd/even styles
    static $row_count;
    if (!isset($row_count))
    {
        $row_count = 1;
    }
    else
    {
        $row_count++;
    }

    ob_start();
    echo '<tr class="' . (($row_count % 2 == 0) ? 'even' : 'odd' ). 'row" ';

    // attach JavaScript handlers
    echo 'onmouseover="highlightTableRow(this)" ';
    echo 'onmouseout="unhighlightTableRow(this)" ';
    echo 'onclick="selectTableRow(\'' . basename($file) . '\', this);" ';
    echo '">';

    // identify appropriate MIME icon to display
    echo '<td style="width:25px; text-align: center;">';
    echo '<img style="height: 16px; width: 16px;" src="img/';
    if ($is_dir && basename($file) == '..')
    {
        echo 'up';
    }
    else if ($is_dir)
    {
        echo 'dir';
    }
    else
    {
        $ext = substr($file, strrpos($file, '.') + 1);
        if (file_exists('img/' . $ext . '.gif'))
        {
            echo $ext;
        }
        else
        {
            echo 'unknown';
        }
    }
    echo '.gif" /></td>';

    // display file information
    echo '<td>' . basename($file) . '</td>';
    if ($show_stats)
    {
        echo '<td>';
        if ($is_dir)
        {
            echo '---';
        }
        else
        {
            echo size_human_read($info['size']);
        }
        echo '</td>';
        echo '<td>' . date('m/d/Y', $info['mtime']) . '</td>';
    }
    else
    {
        echo '<td>&nbsp;</td><td>&nbsp;</td>';
    }
    echo '</tr>';
    $r = ob_get_contents();
    ob_end_clean();

    return $r;
}


if (!isset($_GET['action'])) return;
switch ($_GET['action'])
{
    // return HTML table with directory contents
    case 'list':

        // ensure all necessary parameters are available
        if (!isset($_GET['dir'])) return;

        // prevent users from traversing outside the base directory
        $directory = realpath(BASEDIR . $_GET['dir']);
        if (strpos($directory, BASEDIR) !== 0) return;

        $ds = array();  // directories
        $fs = array();  // files

        if($dir = opendir($directory))
        {
            while($file = basename(readdir($dir)))
            {
                if($file == '.' || $file == '..')
                {
                    continue;
                }

                if (is_dir($directory . '/' . $file))
                {
                    $ds[] = $file;
                }
                else if(is_file($directory . '/' . $file))
                {
                    $fs[] = $file;
                }
            }
            closedir($dir);
        }
        natcasesort($ds);  // natural case-insensitive sort
        natcasesort($fs);
?>
 <table>
  <thead>
   <tr><th colspan="2">File/Folder</th><th>Size</th><th>Date</th></tr>
  </thead>
  <tbody>
<?php
        // don't show .. for root directory
        if (BASEDIR == $directory)
        {
            if (count($ds))
            {
                echo directory_row($directory . '/' . array_shift($ds),
                    TYPE_DIRECTORY, true);
            }
            else if (count($fs))
            {
                echo directory_row($directory . '/' . array_shift($fs),
                    TYPE_FILE, true);
            }
        }
        else
        {
            echo directory_row('..', TYPE_DIRECTORY, false);
        }

        foreach ($ds as $d)
        {
            echo directory_row($directory . '/' . $d, TYPE_DIRECTORY);
        }
        foreach ($fs as $file)
        {
            echo directory_row($directory . '/' . $file, TYPE_FILE);
        }
?>
    </tbody>
   </table>
<?php
        break;

    // delete a directory or file
    case 'delete':
    
        // ensure all necessary parameters are available
        if (!isset($_GET['dir']) || !isset($_GET['file']))
        {
            return;
        }
    
        // prevent users from traversing outside the base directory
        $directory = realpath(BASEDIR . $_GET['dir']);
        if (strpos($directory, BASEDIR) !== 0)
        {
            return;
        }
    
        $target = $directory . '/' . $_GET['file'];
    
        if (file_exists($target))
        {
            if (is_dir($target) && @rmdir($target))
            {
                    echo 'OK';
            }
            else if (is_file($target) && @unlink($target))
            {
                echo 'OK';
            }
            else
            {
                echo 'ERROR';
            }
        }
        else
        {
            echo 'ERROR';
        }
        break;
    
    // rename a directory or file
    case 'rename':
    
        // ensure all necessary parameters are available
        if (!isset($_GET['dir']) || !isset($_GET['oldfile']) ||
            !isset($_GET['newfile']))
        {
            return;
        }
    
        // prevent users from traversing outside the base directory
        $directory = realpath(BASEDIR . $_GET['dir']);
        if (strpos($directory, BASEDIR) !== 0)
        {
            return;
        }
    
        $old = $directory . '/' . $_GET['oldfile'];
        $new = $directory . '/' . $_GET['newfile'];
    
        if (file_exists($old) && @rename($old, $new))
        {
            echo 'OK';
        }
        else
        {
            echo 'ERROR';
        }
        break;
    
    // create a new directory
    case 'new':
    
        // ensure all necessary parameters are available
        if (!isset($_GET['dir']) || !isset($_GET['name']))
        {
            return;
        }
    
        // prevent users from traversing outside the base directory
        $directory = realpath(BASEDIR . $_GET['dir']);
        if (strpos($directory, BASEDIR) !== 0)
        {
            return;
        }
    
        $target = $directory . '/' . $_GET['name'];
    
        if (!file_exists($target) && @mkdir($target))
        {
            echo 'OK';
        }
        else
        {
            echo 'ERROR';
        }
        break;
    
    // return information needed to open a folder or file
    case 'open':
     
        // ensure all necessary parameters are available
        if (!isset($_GET['dir']) || !isset($_GET['file']))
        {
            return;
        }
    
        // prevent users from traversing outside the base directory
        $directory = realpath(BASEDIR . $_GET['dir']);
        if (strpos($directory, BASEDIR) !== 0)
        {
            return;
        }
    
        $target = $directory . '/' . $_GET['file'];
    
        if (file_exists($target))
        {
            if (is_file($target))
            {
                echo json_encode(array(
                    'retType' => 'file'));
            }
            else if (is_dir($target))
            {
                echo json_encode(array(
                    'retType' => 'directory',
                    'directory' => substr($target, strlen(BASEDIR))));
            }
        }
        break;
}
?>