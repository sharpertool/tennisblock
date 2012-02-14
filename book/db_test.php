<?php

    $dbHost = "localhost";
    $dbUser = "fnt_user";
    $dbPass = "P5HJTdHt5dR2t9Q2";
    $dbDatabase = "friday_tennis";

    $db = mysql_connect("$dbHost", "$dbUser", "$dbPass") or die ("Error connecting to database.");
    
    mysql_select_db("$dbDatabase", $db) or die ("Couldn't select the database.");
    
    $result=mysql_query("select * from players order by lastname, firstname", $db);
    
    //check that at least one row was returned
    
    $rowCheck = mysql_num_rows($result);
    if($rowCheck > 0){
        echo "<table>";
        while($row = mysql_fetch_array($result)){
            echo "<tr><td>" . $row['firstname'] . " " . $row['lastname'] . "</td></tr>";
        }
        echo "</table>";
    }
?>