<?php

require('../util/Connection.php');
require('../util/SessionFunction.php');

require('Header.php');


if(!SessionCheck()){
	return;
}

$date = $_POST['date'];
$time = $_POST['time'];

$query = "UPDATE timer SET deadline_date='$date', deadline_time='$time' WHERE 1";
mysqli_query($con,$query);
mysqli_close($con);

echo "<script>window.location.href = '../Timer.php';</script>";

?>
<?php require('Fullui.php');  ?>