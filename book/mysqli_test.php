<?php

    $dbHost = "localhost";
    $dbUser = "fnt_user";
    $dbPass = "P5HJTdHt5dR2t9Q2";
    $dbDatabase = "friday_tennis";

    $si = function_exists('mysqli_connect');
    if ($si) {
        echo "MySQLI appears to be installed correctly <br>\n";
        $conn = @new mysqli($dbHost,$dbUser,$dbPass,$dbDatabase);
        if (mysqli_connect_errno() != 0) {
            $message = mysqli_connect_error();
            echo "Connect error:$message <br>\n";
        } else {
            echo "Connection worked <br>\n";
            $conn->query("SET NAMES 'utf8'");
            $query_str = "select * from players";
            $result = @$conn->query($query_str);
            if ($result == FALSE) {
                $errno = $conn->errno;
                $errmsg = $conn->error;
                echo "Connection failed with: ($errno) $errmsg<br>\n";
                $conn->close();
                exit;
            } else {
                echo <<<EOM
                <table border=1>
                <tr>
                    <td>Name</td>
                    <td>NTRP</td>
                    <td>Micro NTRP</td>
                </tr>
EOM;
                while (($row_data = @$result->fetch_assoc()) != NULL) {
                    echo <<<EOM
                    <tr>
                        <td>{$row_data['firstname']} {$row_data['lastname']}</td>
                        <td>{$row_data['NTRP']}</td>
                        <td>{$row_data['microNTRP']}</td>
                    </tr>
EOM;
                }
                echo <<<EOTABLE
                </table>
                
EOTABLE;
                $conn->close();
            }
        }
        
    } else{
        echo "No MYSQLI installed<br>\n";
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
    }
?>