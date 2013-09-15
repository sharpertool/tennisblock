<?php

	include_once 'inc/dbconninfo.php';

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
            while (($row_data = @$result->fetch_assoc()) != NULL) {
                echo <<<EOM
                <tr>
                    <td>{$row_data['firstname']} {$row_data['lastname']}</td>
                    <td>{$row_data['NTRP']}</td>
                    <td>{$row_data['microNTRP']}</td>
                </tr>
EOM;
            }
            $conn->close();
        }
    }
?>
