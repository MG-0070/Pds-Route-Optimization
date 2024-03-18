<?php
require('../util/Connection.php');
require('../structures/FPS.php');
require('../util/SessionFunction.php');
ini_set('max_execution_time', 3000);

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


// Filter the excel data 
function filterData(&$str){ 
    $str = str_replace("\t", "", $str);
}

$redirect = 1;

try{
	//if (isset($_POST["submit"])){
		$fileName = $_FILES["file"]["tmp_name"];
		if ($_FILES["file"]["size"] > 0) {
			
			$file = fopen($fileName, "r");
			$i = 0;
			$district = -1;
			$name = -1;
			$id = -1;
			$type = -1;
			$demand = -1;
			$longitude = -1;
			$latitude = -1;
			while (($column = fgetcsv($file, 10000, ",")) !== FALSE) {
				if($i>0){
					if($district<0 or $name<0 or $id<0 or $type<0 or $demand<0 or $latitude<0 or $longitude<0){
						echo "You have modified Template Header, please check";
						exit();
					}
					if(!isValidCoordinate($column[$latitude],'latitude') or !isValidCoordinate($column[$longitude],'longitude')){
						echo "Check Latitude and Longitude Value Latitude: ".$column[$latitude]." Longitude: ".$column[$longitude];
						echo "</br>";
						$redirect = 0;
					}

					if(!isStringNumber($column[$demand])){
						echo "Check Demand Value: ".$column[$demand];
						echo "</br>";
						$redirect = 0;
					}
					$FPS = new FPS;
					filterData($column[$district]);
					filterData($column[$latitude]);
					filterData($column[$longitude]);
					filterData($column[$name]);
					filterData($column[$id]);
					filterData($column[$type]);
					filterData($column[$demand]);
					$uniqueid = uniqid("FPS_",);
					$FPS->setUniqueid(substr($uniqueid,0,15));
					$FPS->setDistrict(ucwords(strtolower($column[$district])));
					$FPS->setLatitude($column[$latitude]);
					$FPS->setLongitude($column[$longitude]);
					$FPS->setName($column[$name]);
					$FPS->setId($column[$id]);
					$FPS->setType($column[$type]);
					$FPS->setDemand($column[$demand]);
					$query_check = $FPS->checkEdit($FPS);
					$query_result = mysqli_query($con, $query_check);
					$numrows = mysqli_num_rows($query_result);
					if($numrows==0){
						echo "Error in loading data as FPS id doesn't exist : ".$column[$id];
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
							case "district":
								$district = $j;
								break;
							case "latitude":
								$latitude = $j;
								break;
							case "longitude":
								$longitude = $j;
								break;
							case "name":
								$name = $j;
								break;
							case "id":
								$id = $j;
								break;
							case "type":
								$type = $j;
								break;
							case "demand":
								$demand = $j;
								break;
						}
					}
				}
				$i = $i+1;
			}
		}
	//}
	//else{
	//	echo "Error Please Select .csv file";
	//}
}
catch(Exception $e){
	echo "Error Please check data in  .csv file";
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
			$district = 0;
			$name = 1;
			$id = 2;
			$type = 3;
			$demand = 4;
			$longitude = 5;
			$latitude = 6;
			while (($column = fgetcsv($file, 10000, ",")) !== FALSE) {
				if($i>0){
					$FPS = new FPS;
					filterData($column[$district]);
					filterData($column[$latitude]);
					filterData($column[$longitude]);
					filterData($column[$name]);
					filterData($column[$id]);
					filterData($column[$type]);
					filterData($column[$demand]);
					$uniqueid = uniqid("FPS_",);
					$FPS->setUniqueid(substr($uniqueid,0,15));
					$FPS->setDistrict($column[$district]);
					$FPS->setLatitude($column[$latitude]);
					$FPS->setLongitude($column[$longitude]);
					$FPS->setName($column[$name]);
					$FPS->setId($column[$id]);
					$FPS->setType($column[$type]);
					$FPS->setDemand($column[$demand]);
					$query_check = $FPS->checkEdit($FPS);
					$query_result = mysqli_query($con, $query_check);
					$numrows = mysqli_num_rows($query_result);
					if($numrows==0){
						echo "Error in loading data as FPS id doesn't exist : ".$column[$id];
						echo "</br>";
						$redirect = 0;
					}
					$query_update = $FPS->updateEdit($FPS);
					mysqli_query($con, $query_update);
				}
				else{
					for($j=0;$j<count($column);$j++){
						switch($column[$j]){
							case "state":
								$state = $j;
								break;
							case "district":
								$district = $j;
								break;
							case "latitude":
								$latitude = $j;
								break;
							case "longitude":
								$longitude = $j;
								break;
							case "name":
								$name = $j;
								break;
							case "id":
								$id = $j;
								break;
							case "type":
								$type = $j;
								break;
							case "demand":
								$demand = $j;
								break;
						}
					}
				}
				$i = $i+1;
			}
			if($redirect==1){
				echo "<script>window.location.href = '../FPS.php';</script>";
			}
		}
	//}
	//else{
	//	echo "Error Please Select .csv file";
	//}
}
catch(Exception $e){
	echo "Error Please check data in  .csv file";
}
?>
<?php require('Fullui.php');  ?>