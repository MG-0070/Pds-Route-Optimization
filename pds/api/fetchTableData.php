<?php
require('../util/Connection.php');
require('../structures/District.php');
require('../util/SessionFunction.php');
require('../structures/Login.php');
// Set maximum execution time to 120 seconds
ini_set('max_execution_time', 3600);

if(!SessionCheck()){
	return;
}

$query = "SELECT * FROM optimised_table ORDER BY last_updated DESC LIMIT 1";
$result = mysqli_query($con,$query);
$response = array();
while($row = mysqli_fetch_array($result))
{
	$temp = array();
	$temp["year"] = $row["year"];
	$temp["month"] = $row["month"];
	$temp["id"] = $row["id"];
	$temp["applicable"] = $row["applicable"];
	$temp["last_updated"] = $row["last_updated"];
	array_push($response,$temp);
}

echo json_encode($response);

?>