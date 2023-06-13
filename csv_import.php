<?php
$servername = "c3-database-do-user-914951-0.b.db.ondigitalocean.com";
$username = "doadmin";
$password = "AVNS_UXdKjBYJzYULsF8uJnC";
$port_name = 25060;
$database = "C3_Database";

// Create a connection
$conn = new mysqli($servername, $username, $password, $database, $port_name);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Call the stored procedure
$csvPath = "test.csv";
$oldTable = "analysis_test";
$sql = "CALL import_and_merge_tables('$csvPath', '$oldTable')";

if ($conn->query($sql) === TRUE) {
    echo "Stored procedure executed successfully";
} else {
    echo "Error executing stored procedure: " . $conn->error;
}

// Close the connection
$conn->close();
?>
