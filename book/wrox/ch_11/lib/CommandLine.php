<?php
// extend Exception class for custom exception type
class CommandLineOptionException extends Exception { }

class CommandLine
{
    // define different configuration file types
    const CONFIG_TYPE_PLAIN = 1;
    const CONFIG_TYPE_INI = 2;

    // accept array of command line arguments, optional array of
    // valid/whitelist options
    static public function parseOptions($args, $allowed = array())
    {
        $options = array();
        $count = count($args);

        // retrive arguments and populate $options array
        for ($i = 1; $i < $count; $i++)
        {
            // retrieve arguments in form of --abc=foo
            if (preg_match('/^--([-A-Z0-9]+)=(.+)$/i', $args[$i], $matches))
            {
                if (empty($allowed) || in_array($matches[1], $allowed))
                {
                    $options[$matches[1]] = $matches[2];
                }
                else
                {
                    throw new CommandLineOptionException(
                        'Unrecognized option ' . $matches[1]);
                }
            }

            // retrieve --abc arguments
            else if (substr($args[$i], 0, 2) == '--')
            {
                $tmp = substr($args[$i], 2);
                if (empty($allowed) || in_array($tmp, $allowed))
                {
                    $options[$tmp] = true;
                }
                else
                {
                    throw new CommandLineOptionException(
                        'Unrecognized option ' . $tmp);
                }
            }

            // retrieve -abc foo, -abc, -a foo and -a arguments
            else if ($args[$i][0] == '-' && strlen($args[$i]) > 1)
            {
                // set all arguments to true except for last in sequence
                for ($j = 1; $j < strlen($args[$i]) - 1; $j++)
                {
                    if (empty($allowed) || in_array($args[$i][$j], $allowed))
                    {
                        $options[$args[$i][$j]] = true;
                    }
                    else
                    {
                        throw new CommandLineOptionException(
                            'Unrecognized option ' . $args[$i][$j]);
                    }
                }

                // set last argument in compressed sequence
                $tmp = substr($args[$i], -1, 1);
                if (empty($allowed) || in_array($tmp, $allowed))
                {
                    // assign next $args value if is value
                    if ($i + 1 < $count && $args[$i + 1][0] != '-')
                    {
                        $options[$tmp] = $args[$i + 1];
                        $i++;
                    }
                    // assign option as boolean
                    else
                    {
                        $options[$tmp] = true;
                    }
                }
                else
                {
                    throw new CommandLineOptionException(
                        'Unrecognized option ' . $tmp);
                }
            }

            // invalid option format
            else
            {
                throw new CommandLineOptionException(
                    'Invalid option format at ' . $args[$i]);
            }
        }

        return $options;
    }

    // process a configuration file and return its options as an array
    static public function parseConfigFile($file, $type = CONFIG_TYPE_PLAIN)
    {
        $options = array();

        // process plain configuration file
        if ($type == CONFIG_TYPE_PLAIN)
        {
            $fp = fopen($file, 'r');
            while (!feof($fp))
            {
                $line = trim(fgets($fp));
                // skip blank lines and comments
                if ($line && !preg('^#', $line))
                {
                    $pieces = explode('=', $line);
                    $opt = trim($pieces[0]);
                    $value = trim($pieces[1]);
    
                    $options[$opt] = $value;
                }
            }
            fclose($fp);
        }

        // process ini configuration file
        else if ($type == CONFIG_TYPE_INI)
        {
            $options = parse_ini_file($file);
        }
        return $options;
    }

    // prompt for user input, accept optional maximum input length and 
    // callback function for validation
    static public function prompt($label, $length = 255, $callback = null)
    {
        echo $label . ': ';
        $value = trim(fread(STDIN, 255));
    
        return ($callback) ? call_user_func($callback, $value) : $value;
    }

    // prompt for user input, accept optional default value, maximum input
    // length and callback function for validation
    static public function promptDefault($label, $default = null, 
        $length = 255, $callback = null)
    {
        $label .= ' [' . $default .']';
        $value = self::prompt($label, $length);

        if (!$value)
        {
            $value = $default;
        }
    
        return ($callback) ? call_user_func($callback, $value) : $value;
    }

}
?>