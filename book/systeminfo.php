<html>
<body>
<table width='100%' border='1'>

<?php

  foreach ($_SERVER as $key => $value)
  {
    echo <<<EOT

<tr>
  <td width='25%'>
     <b>$key</b>
  </td>
  <td>
     $value
  </td>
</tr>
EOT;
  }

?>
</table>
<br/><br/>
</body>
</html>


