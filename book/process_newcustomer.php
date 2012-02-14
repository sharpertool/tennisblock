<html>
<head>
  <title>Welcome !!!</title>
</head>

<body>
<?php
  $fullName = $_POST["fullname"];
  $userName = $_POST["username"];
?>

  <br/><br/>
  <p align='center'>
    Welcome new customer!  You have entered the following information:
  </p>

  <p align='center'>
    Full Name: <b> <?php echo $fullName; ?> </b><br/>
    User Name: <b> <?php echo $userName; ?> </b><br/>
  </p>

</body>
</html>
