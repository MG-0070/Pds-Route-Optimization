<?php
require('../util/Connection.php');
require('../structures/District.php');
require('../util/SessionFunction.php');
require('../structures/Login.php');

if(!SessionCheck()){
	return;
}

$reviewed = "";
$approved = "";

if(isset($_POST['approved'])){
	$approved = $_POST['approved'];
}

if(isset($_POST['reviewed'])){
	$reviewed = $_POST['reviewed'];
}

$month = $_POST['month'];
$district = $_POST['district'];

$parts = explode('_', $month);

$month = $parts[0];
$year = $parts[1]; 
$query = "SELECT * FROM optimised_table WHERE month='$month' AND year='$year'";
$result = mysqli_query($con,$query);
$numrow = mysqli_num_rows($result);
$id = "";
if($numrow>0){
	$row = mysqli_fetch_assoc($result);
	$id = $row['id'];
}

$tablename = "optimiseddata_".$id;


$query = "SHOW TABLES LIKE '$tablename'";
$result = $con->query($query);
$data = null;

if ($result && $result->num_rows > 0) {
	$query = "SELECT * FROM ".$tablename." WHERE to_district='$district'";
	if($reviewed=="reviewed"){
		$query = "SELECT * FROM ".$tablename." WHERE reviewed='yes'";
	}
	else if($reviewed=="notreviewed"){
		$query = "SELECT * FROM ".$tablename." WHERE reviewed = '' OR reviewed IS NULL";
	}

	if($approved=="approved"){
		$query = "SELECT * FROM ".$tablename." WHERE approve='yes'";
	}
	else if($approved=="notapproved"){
		$query = "SELECT * FROM ".$tablename." WHERE approve='no' or approve IS NULL";
	}
	
	$result = mysqli_query($con,$query);
	while($row = mysqli_fetch_assoc($result))
	{
		$data[] = $row;
	}

	$query_warehouse = "SELECT id from warehouse WHERE active='1'";
	$result_warehouse = mysqli_query($con,$query_warehouse);
	while($row_warehouse = mysqli_fetch_assoc($result_warehouse)){
		$warehouse[] = $row_warehouse;
	}
	$resultarray = [];
	if($data==null){
		$data = array();
	}
	$resultarray["data"] = $data;
	$resultarray["warehouse"] = $warehouse;
	
	echo json_encode($resultarray);
} else {
	$resultarray = [];
	$resultarray["data"] = array();
	$resultarray["warehouse"] = array();
	echo json_encode($resultarray);
}
?>