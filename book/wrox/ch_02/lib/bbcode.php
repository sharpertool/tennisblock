<?php
// format text marked up with BBCode tags to HTML-- see
// http://www.phpbb.com/community/faq.php?mode=bbcode for more information.
function format_bbcode($string)
{
    // internal function to replace BBCode tags with suitable HTML
    function _format_bbcode($string)
    {
        // use regular expression to identify and break apart BBCode tags
        while (preg_match('|\[([a-z]+)=?(.*?)\](.*?)\[/\1\]|', $string, $part,
            PREG_OFFSET_CAPTURE))
        {
            $part[2][0] = str_replace('"', "", $part[2][0]);
            $part[2][0] = str_replace("'", "", $part[2][0]);
            $part[3][0] = _format_bbcode($part[3][0]);
            switch ($part[1][0])
            {
                // process bold, italic and underline elements
                case 'b':
                case 'i':
                case 'u':
                    $replace = sprintf('<%s>%s</%s>', $part[1][0], $part[3][0],
                        $part[1][0]);
                    break;

                // process code element
                case 'code':
                    $replace = '<pre>' . $part[3][0] . '</pre>';
                    break;

                // process color styling                    
                case 'color':
                    $replace = sprintf('<span style="color: %s">%s</span>',
                        $part[2][0], $part[3][0]);
                    break;

                // process email element
                case 'email':
                    $replace = sprintf('<a href="mailto:%s">%s<\a>',
                        $part[3][0], $part[3][0]);
                    break;

                // process size styling
                case 'size':
                    $replace = sprintf('<span style="font-size: %s">%s</span>',
                        $part[2][0], $part[3][0]);
                    break;

                // process quotes
                case 'quote':
                    $replace = (empty($part[2][0])) ?
                        ('<blockquote><p>' . $part[3][0] .
                            '</p></blockquote>') :
                        sprintf('<blockquote><p>%s wrote:<br />%s</p>' .
                            '</blockquote>', $part[2][0], $part[3][0]);
                    break;

                // process image element
                case 'img':
                    $replace = '<img src="' . $part[3][0] . '" alt=""/>';
                    break;

                // process hyperlink
                case 'url':
                    $replace = sprintf('<a href="%s">%s</a>', 
                        (!empty($part[2][0])) ? $part[2][0] : $part[3][0],
                        $part[3][0]));
                    break;

                // process bulleted lists
                case 'list':
                    $replace = str_replace('[*]', '</li><li>', $part[3][0]);
                    $replace = '<x>' . $replace;
                    switch ($part[2][0])
                    {
                        case '1':
                            $replace = str_replace('<x></li>',
                                '<ol style="list-style-type: decimal">',
                                $replace . '</ol>');
                            break;

                        case 'A':
                            $replace = str_replace('<x></li>',
                                '<ol style="list-style-type: upper-alpha">',
                                $replace . '</ol>');
                            break;

                        case 'a':
                            $replace = str_replace('<x></li>',
                                '<ol style="list-style-type: lower-alpha">',
                                $replace . '</ol>');
                            break;

                        default:
                            $replace = str_replace('<x></li>',
                                '<ul>', $replace . '</ul>');
                            break;
                    }
                    break;

                default:
                    $replace = $part[3][0];
                    break;
            }
            $string = substr_replace($string, $replace, $part[0][1],
                strlen($part[0][0]));
        }
        return $string;
    }

    // replace tags
    $string = _format_bbcode($string);

    // clean up line endings and add paragraph and line break tags
    $string = str_replace("\r\n\r\n", '</p><p>', $string);
    $string = str_replace("\n\n", '</p><p>', $string);
    $string = str_replace("\r\n", '<br />', $string);
    $string = str_replace("\n", '<br />', $string);
    $string = '<p>' . $string . '</p>';
    
    return $string;
}
?>
