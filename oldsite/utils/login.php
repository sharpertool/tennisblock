<?PHP
    //check that the user is calling the page from the login form and not accessing it directly
    //and redirect back to the login form if necessary
    
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    if (!isset($username) || !isset($password)) {
        header( "Location: login.html" );
        //check that the form fields are not empty, and redirect back to the login page if they are
    } elseif (empty($username) || empty($password)) {
        header( "Location: login.html" );
    } else { 

        //convert the field values to simple variables
        
        //add slashes to the username and md5() the password
        $user = addslashes($_POST['username']);
        $pass = md5($_POST['password']);
        
        
        //set the database connection variables
        include_once '../inc/dbconninfo.php';
        
        //connet to the database
        
        $db = mysql_connect("$dbHost", "$dbUser", "$dbPass") or die ("Error connecting to database.");
        
        mysql_select_db("$dbDatabase", $db) or die ("Couldn't select the database.");
        
        $result=mysql_query("select * from users where username='$user' AND password='$pass'", $db);
        
        //check that at least one row was returned
        
        $rowCheck = mysql_num_rows($result);
        if($rowCheck > 0){
            while($row = mysql_fetch_array($result)){
            
                //start the session and register a variable
              
                session_start();
                $_SESSION['username'] = $user;
              
                //successful login code will go here...
                echo 'Success!';
              
                //we will redirect the user to another page where we will make sure they're logged in
                header( "Location: index.php" );
              
            }
            
        } else {
        
            //if nothing is returned by the query, unsuccessful login code goes here...
          
            echo 'Incorrect login name or password. Please try again.';
        }
    }
    mysql_freeresult($result);
    mysql_close($db);
?>
