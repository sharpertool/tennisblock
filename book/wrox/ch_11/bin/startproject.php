#! /usr/bin/php
<?php
// include shared code
include '../lib/CommandLine.php';

// define location of the skeleton layout
define('SKEL_FILES', '/path/to/skeleton/layout');

// function to output the version number
function show_version()
{
    echo basename($_SERVER['argv'][0]) . ' version 1.0' . "\n";
}

// function to output usage instructions
function show_help($display = true) 
{
    $script = basename($_SERVER['argv'][0]);
    $help =  <<<ENDHELP
Usage: {$script} [OPTIONS]
Setup project directory and copy basic files into it.

-c, --copy-only      copy project skeleton to TARGET but do not replace
                     Placeholders or delete .tmp files
-h, --help           display this help and exit
-o, --output=TARGET  specify directory where the files will be copied
-p, --preserve       don't delete .tmp files after replacing placeholders
-v, --version        print version information and exit

ENDHELP;
    if ($display)
    {
        echo $help;
    }
    else
    {
        return $help;
    }
}

// function to recursively copy a directory, modified from code found
// at http://us2.php.net/manual/en/function.copy.php#77238
function dircopy_recurs($source, $dest)
{
    if (!$dir = opendir($source))
    {
        fwrite(STEDRR, 'ERROR: Unable to open ' . $source . "\n");
        exit(1);
    }

    while($file = readdir($dir))
    {
        if($file != '.' && $file != '..')
        {
            $path = $source . '/' . $file;

            // create directory and copy contents
            if (is_dir($path))
            {
                if(!mkdir($dest . '/' . $file))
                {
                    fwrite(STDERR, 'ERROR: Unable to create directory ' .
                       $file . '.' . "\n");
                    exit(1);
                }
                dircopy_recurs($path, $dest . '/' . $file);
            }
            // copy files
            else if(is_file($path))
            {
                if(!copy($path, $dest . '/' . $file))
                {
                    fwrite(STDERR, 'ERROR: Unable to copy file ' . $file .
                        '.' . "\n");
                    exit(1);
                }
            }
        }
    }
    closedir($dir);
}

// no arguments provided
if ($_SERVER['argc'] == 1)
{
    fwrite(STDERR, show_help(false));
    exit(1);
}

// Retrieve command-line arguments
else
{
    $allowed = array('c', 'copy-only', 'h', 'help', 'o', 'output', 
        'p', 'preserve', 'v', 'version');
    try
    {
        $options = CommandLine::parseOptions($_SERVER['argv'], $allowed);
    }
    catch (CommandLineOptionException $e)
    {
        fwrite(STDERR, $e->getMessage() . "\n" . show_help(false));
        exit(1);
    }
}

// show help if requested
if (isset($options['h']) || isset($options['help']))
{
    show_help();
    exit();
}

// show version information if requested
if (isset($options['v']) || isset($options['version']))
{
    show_version();
    exit();
}

// retrieve target directory
if (isset($options['o']) && isset($options['output']))
{
    fwrite(STDERR, 'ERROR: Unable to determine target.  To prevent ' . 
        'potential ' . "\n" . 'conflicts please use either -o or ' .
        '--output, not both.' . "\n");
    exit(1);
}
else if (isset($options['o']) || isset($options['output']))
{
    $output = (isset($options['o'])) ? $options['o'] : $options['output'];
}
else
{
    fwrite(STDERR, 'ERROR: Target location was not specified with -o ' . 
        'or --output.' . "\n");
    exit(1);
}

// determine absolute path to target
$dir = basename($output);
$path = realpath(substr($output, 0, strlen($output) - strlen($dir)));

// determine target can be created and doesn't already exist
clearstatcache();
if (!file_exists($path) || !is_dir($path) || !is_writable($path))
{
    fwrite(STDERR, 'ERROR: Parent of target directory either does ' .
        'not exist or is' . "\n" . 'not writable.' . "\n");
    exit(1);
}
if (file_exists($path . '/' . $dir))
{
    fwrite(STDERR, 'ERROR: Requested target already exists.' . "\n");
    exit(1);
}

do
{
    // Retrieve configuration information
    $db_host = CommandLine::promptDefault('Database host', 'localhost');
    $db_schema = CommandLine::promptDefault('Database schema', 'TEST');
    $db_user = CommandLine::promptDefault('Database user', 'TESTUSR');
    $db_pass = CommandLine::prompt('Database password');
    $db_tbl_prefix = CommandLine::promptDefault('Database table prefix', '');

    // Verify collected information is all correct
    echo str_repeat('-', 70) . "\n";
    echo 'Database host:          ' . $db_host . "\n";
    echo 'Database schema:        ' . $db_schema . "\n";
    echo 'Database user:          ' . $db_user . "\n";
    echo 'Database password:      ' . $db_pass . "\n";
    echo 'Database table prefix:  ' . $db_tbl_prefix . "\n";

    $ok = CommandLine::promptDefault('Is this correct?', 'yes', 3,
        'strtolower');
}
while ($ok != 'yes' && $ok != 'y');
echo "\n";

// Create the target directory
if (!mkdir($path . '/' . $dir))
{
    fwrite(STDERR, 'ERROR: Unable to create target directory.' . "\n");
    exit(1);
}

// copy the skeleton files to the target directory
dircopy_recurs(SKEL_FILES, $path . '/' . $dir);

// match up placeholders with user provided values to replace them in the
// temporary files and rename them as permanent
if (!isset($options['c']) && !isset($options['copy-only']))
{
    $tags = array(
        '<tag::db_host>' => $db_host,
        '<tag::db_schema>' => $db_schema,
        '<tag::db_user>' => $db_user,
        '<tag::db_pass>' => $db_pass, 
        '<tag::db_tbl_prefix>' => $db_tbl_prefix);

    $files = array(
	       'lib/db.php.tmp');

    foreach ($files as $f)
    {
        $file_old = $path . '/' . $dir . '/' . $f;
        $file_new = substr($file_old, 0, -4);
        $newcontents = str_replace(array_keys($tags),
				    array_values($tags),
				    file_get_contents($file_old));
        if (!file_put_contents($file_new, $newcontents))
        {
            fwrite(STDERR, 'ERROR: Unable to write ' . $file_new . '.' . "\n");
            exit(1);
        }

        // remove tmp files
        if (!isset($options['p']) && !isset($options['preserve']))
        {
            if (!unlink($file_old))
            {
                fwrite(STDERR, 'ERROR: Unable to remove ' . $file_old . '.' .
                    "\n");
                fclose($fp);
                exit(1);
            }
        }
    }
}

echo 'Congratulations!  Your project has been deployed to ' . "\n" .
    $path . '/' . $dir . ".\n\n";
?>