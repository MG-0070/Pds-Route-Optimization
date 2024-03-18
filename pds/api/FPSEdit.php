<?php

require('../util/Connection.php');
require('../structures/FPS.php');
require('../util/SessionFunction.php');
require('../structures/Login.php');

if(!SessionCheck()){
	return;
}

require('Header.php');


function formatName($name) {
	$name = preg_replace('/[^a-zA-Z0-9_ ]/', '', $name);
    $name = ucwords(strtolower($name));
    return trim($name);
}

function isValidCoordinate($value, $coordinateType) {
    // Check if the value is a number and not a string
    if (!is_numeric($value)) {
        return false;
    }
	
    // Convert the value to a float
    $coordinate = floatval($value);

    // Check if it's latitude or longitude and validate within the range
    switch ($coordinateType) {
        case 'latitude':
            return ($coordinate >= -90 && $coordinate <= 90);
        case 'longitude':
            return ($coordinate >= -180 && $coordinate <= 180);
        default:
            return false;
    }
}

function isStringNumber($stringValue) {
    return is_numeric($stringValue);
}

$person = new Login;
$person->setUsername($_POST["username"]);
$person->setPassword($_POST["password"]);

$query = "SELECT * FROM login WHERE username='".$person->getUsername()."' AND password='".$person->getPassword()."'";
$result = mysqli_query($con,$query);
$numrows = mysqli_num_rows($result);

if($numrows == 0){
	echo "Password or Username is incorrect";
	return;
}

if(!isValidCoordinate($_POST["latitude"],'latitude') or !isValidCoordinate($_POST["longitude"],'longitude')){
	echo "Check Latitude and Longitude Value";
	exit();
}

if(!isStringNumber($_POST["demand"])){
	echo "Check Demand Value";
	exit();
}

$district = formatName($_POST["district"]);
$latitude = $_POST["latitude"];
$longitude = $_POST["longitude"];
$name = formatName($_POST["name"]);
$id = $_POST["id"];
$type = $_POST["type"];
$demand = $_POST["demand"];
$uniqueid = $_POST["uniqueid"];

$FPS = new FPS;
$FPS->setUniqueid($uniqueid);
$FPS->setDistrict($district);
$FPS->setLatitude($latitude);
$FPS->setLongitude($longitude);
$FPS->setName($name);
$FPS->setId($id);
$FPS->setType($type);
$FPS->setDemand($demand);

$query_check = $FPS->checkInsert($FPS);
$query_result = mysqli_query($con, $query_check);
$numrows = mysqli_num_rows($query_result);
if($numrows!=0){
	$row = mysqli_fetch_assoc($query_result);
	$uniqueid_check = $row["uniqueid"];
	if($uniqueid!=$uniqueid_check){
		echo "Error in updating data as FPS id already exist ID: ".$id;
		echo "</br>";
		exit();
	}
}

$query = $FPS->update($FPS);
mysqli_query($con, $query);

mysqli_close($con);

echo "<script>window.location.href = '../FPS.php';</script>";


?>
<?php require('Fullui.php');  ?>