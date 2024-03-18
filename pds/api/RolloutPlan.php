<?php
require('../util/Connection.php');
require('../util/SessionCheck.php');

require('Header.php');

$query = "SELECT * FROM optimised_table ORDER BY last_updated DESC LIMIT 1";
$result = mysqli_query($con,$query);
$response = array();
$id = "";
while($row = mysqli_fetch_array($result))
{
	$id= $row["id"];
}


$tablename = "optimiseddata_".$id;

$query = "SELECT * FROM $tablename WHERE 1";
$result = mysqli_query($con,$query);
$numrows = mysqli_num_rows($result);
if($numrows>0){
	while($row = mysqli_fetch_assoc($result)){
		$temp = $row['new_id_admin'];
		$fromid_temp = $row['from_id'];
		$to_id = $row['to_id'];
		if($temp!=null and strlen($temp)>0){
			$query = "UPDATE $tablename SET from_id='$temp', old_id='$fromid_temp', new_id_admin='' WHERE from_id='$fromid_temp' AND to_id='$to_id'";
			mysqli_query($con,$query);
		}
	}
}

$query = "UPDATE optimised_table SET rolled_out='1' WHERE id='$id'";
mysqli_query($con,$query);

mysqli_close($con);

echo "<script>window.location.href = '../OptimisedData.php';</script>";

?>
<?php require('Fullui.php');  ?>