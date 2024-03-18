<?php
require('../util/Connection.php');
require('../structures/Warehouse.php');
require('../util/SessionFunction.php');
ini_set('max_execution_time', 3000);

require('Header.php');

$mapData = [
    "District" => "district",
    "Name of Warehouse" => "name",
    "Warehouse ID" => "id",
    "Motorable/Non-Motorable" => "type",
    "Warehouse Type" => "warehousetype",
    "Latitude" => "latitude",
    "Longitude" => "longitude",
    "Storage" => "storage"
];

// Reverse mapping
$reverseMapData = array_flip($mapData);

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

$redirect = 1;

try{
	$fileName = $_FILES["file"]["tmp_name"];
	if ($_FILES["file"]["size"] > 0) {
		$file = fopen($fileName, "r");
		$i = 0;
		$latitude = -1;
		$longitude = -1;
		$storage = -1;
		while (($column = fgetcsv($file, 10000, ",")) !== FALSE) {
			if($i>0){
				if($storage<0 or $latitude<0 or $longitude<0){
					echo "You have modified Template Header, please check";
					exit();
				}
				if(!isValidCoordinate($column[$latitude],'latitude') or !isValidCoordinate($column[$longitude],'longitude')){
					echo "Check Latitude and Longitude Value Latitude: ".$column[$latitude]." Longitude: ".$column[$longitude];
					echo "</br>";
					$redirect = 0;
				}

				if(!isStringNumber($column[$storage])){
					echo "Check Storage Value: ".$column[$storage];
					echo "</br>";
					$redirect = 0;
				}
			}
			else{
				for($j=0;$j<count($column);$j++){
					switch($column[$j]){
						case "state":
							$state = $j;
							break;
						case $reverseMapData["district"]:
							$district = $j;
							break;
						case $reverseMapData["latitude"]:
							$latitude = $j;
							break;
						case $reverseMapData["longitude"]:
							$longitude = $j;
							break;
						case $reverseMapData["name"]:
							$name = $j;
							break;
						case $reverseMapData["id"]:
							$id = $j;
							break;
						case $reverseMapData["type"]:
							$type = $j;
							break;
						case $reverseMapData["storage"]:
							$storage = $j;
							break;
						case $reverseMapData["warehousetype"]:
							$warehousetype = $j;
							break;
					}
				}
			}
			$i = $i+1;
		}
	}
}
catch(Exception $e){
	echo "Error Please check data in  .csv file";
	exit();
}

if($redirect==0){
	exit();
}

try{
	//if (isset($_POST["submit"])){
		$fileName = $_FILES["file"]["tmp_name"];
		if ($_FILES["file"]["size"] > 0) {
			
			$file = fopen($fileName, "r");
			$i = 0;
			$district = -1;
			$name = -1;
			$id = -2;
			$warehousetype = -3;
			$type = -4;
			$latitude = -5;
			$longitude = -6;
			$storage = -7;
			while (($column = fgetcsv($file, 10000, ",")) !== FALSE) {
				if($i>0){
					if($district<0 or $name<0 or $id<0 or $type<0 or $storage<0 or $latitude<0 or $longitude<0 or $warehousetype<0){
						echo "You have modified Template Header, please check";
						exit();
					}
					$Warehouse = new Warehouse;
					$uniqueid = uniqid("WH_",);
					$Warehouse->setUniqueid(substr($uniqueid,0,15));
					$Warehouse->setDistrict(ucwords(strtolower($column[$district])));
					$Warehouse->setLatitude($column[$latitude]);
					$Warehouse->setLongitude($column[$longitude]);
					$Warehouse->setName($column[$name]);
					$Warehouse->setId($column[$id]);
					$Warehouse->setType($column[$type]);
					$Warehouse->setStorage($column[$storage]);
					$Warehouse->setWarehousetype($column[$warehousetype]);
					while(true){
						$query_check = $Warehouse->check($Warehouse);
						$query_result = mysqli_query($con, $query_check);
						$numrows = mysqli_num_rows($query_result);
						if($numrows==0){
							break;
						}
						else{
							$uniqueid = uniqid("WH_",);
							$Warehouse->setUniqueid(substr($uniqueid,0,15));
						}
					}
					$query_insert_check = $Warehouse->checkInsert($Warehouse);
					$query_insert_result = mysqli_query($con, $query_insert_check);
					$numrows_insert = mysqli_num_rows($query_insert_result);
					if($numrows_insert==0){
						$query_add = $Warehouse->insert($Warehouse);
						mysqli_query($con, $query_add);
					}
					else{
						echo "Warehouse with id ".$Warehouse->getId()." Already Exist</br>";
						$redirect = 2;
					}
				}
				else{
					for($j=0;$j<count($column);$j++){
						switch($column[$j]){
							case "state":
								$state = $j;
								break;
							case $reverseMapData["district"]:
								$district = $j;
								break;
							case $reverseMapData["latitude"]:
								$latitude = $j;
								break;
							case $reverseMapData["longitude"]:
								$longitude = $j;
								break;
							case $reverseMapData["name"]:
								$name = $j;
								break;
							case $reverseMapData["id"]:
								$id = $j;
								break;
							case $reverseMapData["type"]:
								$type = $j;
								break;
							case $reverseMapData["storage"]:
								$storage = $j;
								break;
							case $reverseMapData["warehousetype"]:
								$warehousetype = $j;
								break;
						}
					}
				}
				$i = $i+1;
			}
			if($redirect==1){
				echo "<script>window.location.href = '../Warehouse.php';</script>";
			}
		}
	//}
	//else{
		//echo "Error Please Select .csv file";
	//}
}
catch(Exception $e){
	echo "Error Please check data in  .csv file";
}
?>
<?php require('Fullui.php');  ?>