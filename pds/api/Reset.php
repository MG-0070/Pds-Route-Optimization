<?php
require('../util/Connection.php');
require('../structures/Login.php');

require('Header.php');

$newpassword = $_POST['newpassword'];
$confirmpassword = $_POST['confirmpassword'];

if($newpassword=="" || $confirmpassword==""){
	echo "Password is Empty";
	return;
}
if($newpassword!=$confirmpassword){
	echo "Both Password doesn't match";
	return;
}

$person = new Login;
$person->setUsername($_POST["username"]);
$person->setPassword($_POST["oldpassword"]);

$query = "SELECT * FROM login WHERE username='".$person->getUsername()."' AND password='".$person->getPassword()."'";
$result = mysqli_query($con,$query);
$numrows = mysqli_num_rows($result);

if($numrows == 0){
	echo "Old Password and username is incorrect";
}
else if($numrows > 0){
	$query1 = "UPDATE login SET password='$newpassword' WHERE 1";
	mysqli_query($con,$query1);

	mysqli_close($con);
	echo "<script>window.location.href = '../Login.php';</script>";

}
?>
<?php require('Fullui.php');  ?>