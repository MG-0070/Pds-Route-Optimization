<?php
require('../util/Connection.php');

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

// Filter the excel data 
function filterData(&$str){ 
    $str = preg_replace("/\t/", "\\t", $str); 
    $str = preg_replace("/\r?\n/", "\\n", $str); 
    if(strstr($str, '"')) $str = '"' . str_replace('"', '""', $str) . '"'; 
}

// Excel file name for download 
$fileName = "WarehouseData_" . date('d-m-Y') . ".csv"; 

$columns = array();

$query = "SHOW COLUMNS FROM warehouse";
$result = mysqli_query($con,$query);
$numrows = mysqli_num_rows($result);
if($numrows>0){
	while($row = mysqli_fetch_array($result)){
		if($row['Field']!="uniqueid" and $row['Field']!="active"){
			array_push($columns,$reverseMapData[$row['Field']]);
		}
	}
}

// Display column names as first row 
$excelDataColumns = implode(",", array_values($columns)) . "\n";

// Render excel data 
echo $excelDataColumns;

$query = "SELECT * FROM warehouse WHERE 1";
$result = mysqli_query($con,$query);
$numrows = mysqli_num_rows($result);
if($numrows>0){
	while($row = mysqli_fetch_array($result)){
		for($i=0;$i<count($columns);$i++){
			if ($columns[$i] !== "uniqueid" or $columns[$i]!="active") {
				filterData($row[$mapData[$columns[$i]]]);
				echo "\t".$row[$mapData[$columns[$i]]] . ',';
            }
        }
		echo "\n";
	}
}


// Headers for download 
header('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
header('Content-Disposition: attachment;filename="' . $fileName . '"');
header('Cache-Control: max-age=0');

exit();

?>