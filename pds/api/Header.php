<?php

?>

<!DOCTYPE html>
<html lang="en">
    <head>
		<title>PDS Admin</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<meta name="theme-color" content="#ffffff">
        <link rel="stylesheet" type="text/css" id="theme" href="../css/theme-black.css"/>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">

		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
								
		<style>
		.popup {
			display: none;
			position: fixed;
			top: 50%;
			left: 50%;
			transform: translate(-50%, -50%);
			padding: 20px;
			background-color: #fff;
			box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
			z-index: 1000;
			font-family: sans-serif;
		}
		.x-navigation li a:hover,
		.page-sidebar.scroll a:hover {
			background-color: #EA743E;
			color: #fff;
		}
		.x-navigation .xn-openable > a {
			background-color: #FF5733;
			color: #fff;
		}
		.x-navigation .xn-openable ul li a:hover {
			background-color: #9240FF; 
			color: #fff;
			padding-left: 20px;
		}
		.x-navigation .xn-openable ul li {
			padding-bottom: 5px;
		}
		.red-bg-gap {
			background-color: red;
			padding: 10px;
			margin-bottom: 10px;
		}
		</style>
		<!-- START PLUGINS -->
         <script type="text/javascript" src="../js/plugins/jquery/jquery.min.js"></script>
        <script type="text/javascript" src="../js/plugins/jquery/jquery-ui.min.js"></script>
        <script type="text/javascript" src="../js/plugins/bootstrap/bootstrap.min.js"></script>
        <!-- END PLUGINS -->

        <!-- THIS PAGE PLUGINS -->
        <script type='text/javascript' src='../js/plugins/icheck/icheck.min.js'></script>
        <script type="text/javascript" src="../js/plugins/mcustomscrollbar/jquery.mCustomScrollbar.min.js"></script>
        <script type="text/javascript" src="../js/plugins/datatables/jquery.dataTables.min.js"></script>
		<script type="text/javascript" src="../js/plugins/tableexport/tableExport.js"></script>
		<script type="text/javascript" src="../js/plugins/tableexport/jquery.base64.js"></script>
		<script type="text/javascript" src="../js/plugins/tableexport/html2canvas.js"></script>
		<script type="text/javascript" src="../js/plugins/tableexport/jspdf/libs/sprintf.js"></script>
		<script type="text/javascript" src="../js/plugins/tableexport/jspdf/jspdf.js"></script>
		<script type="text/javascript" src="../js/plugins/tableexport/jspdf/libs/base64.js"></script>
		
		
        <script type="text/javascript" src="../js/plugins.js"></script>
        <script type="text/javascript" src="../js/actions.js"></script>
        <!-- END PAGE PLUGINS -->
		

    </head>
    <body>
        <!-- START PAGE CONTAINER -->
		<div class="page-container">
        <!-- START PAGE SIDEBAR -->
        <div class="page-sidebar scroll">
            <!-- START X-NAVIGATION -->
			<ul class="x-navigation">
				<li class="xn-logo">
					<span style="font-size: 20px; text-align: center; margin: 10px;color:#fff">Punjab State Level</span>
					<a href="#" class="x-navigation-control"></a>
				</li>
				<li class="xn-profile">
					<div class="profile">
						<div class="profile-data">
							<div class="profile-data-name">
								<!-- <b>Namaste</b> -->
								<b>
									<img src="../img/PngItem_1109026.png" alt="Logo" style="vertical-align: middle; height: 60px; width: 60px;" /> Namaste
								</b>
							</div>
						</div>
					</div>
				</li>
				<li>
					<a href="../Home.php"><i class="fa fa-home"></i> <span class="xn-text" style="font-family:sans-serif;font-weight:italic;font-size:18px;">Home</span></a>
				</li>
				<li>
					<a href="../OptimisedData.php.php"><i class="fa fa-info"></i> <span class="xn-text" style="font-family:sans-serif;font-weight:italic;font-size:18px;">Optimised Planning</span></a>
				</li>
				<li>
					<a href="../RolloutPlan.php"><i class="fa fa-info"></i> <span class="xn-text" style="font-family:sans-serif;font-weight:italic;font-size:18px;">Rollout Plan</span></a>
				</li>
				<li>
					<a href="../api/Logout.php"><i class="fa fa-minus"></i> <span class="xn-text" style="font-family:sans-serif;font-weight:italic;font-size:18px;">Logout</span></a>
				</li>
				<li class="xn-openable">
					<a href="#"><i class="fas fa-edit"></i> <span class="xn-text" style="font-family:sans-serif;font-weight:italic;font-size:18px;">Edit PDS Details</span></a>
					<ul style="background-color:#000">
						<li><a href="../District.php"><i class="fa fa-edit"></i> <span class="xn-text" style="font-family:sans-serif;font-weight:italic;font-size:18px;">Edit Districts</span></a></li>
						<li><a href="../Warehouse.php"><i class="fa fa-edit"></i> <span class="xn-text" style="font-family:sans-serif;font-weight:italic;font-size:18px;">Edit Warehouse</span></a></li>
						<li><a href="../FPS.php"><i class="fa fa-edit"></i> <span class="xn-text" style="font-family:sans-serif;font-weight:italic;font-size:18px;">Edit FPS</span></a></li>
						<li><a href="../Userdata.php"><i class="fa fa-edit"></i> <span class="xn-text" style="font-family:sans-serif;font-weight:italic;font-size:18px;">User Data</span></a></li>
					</ul>
				</li>
				<li style="margin-bottom: 60px;">
					<a><i class="fa fa-pencil-square"></i> <span class="xn-text" style="font-family:sans-serif;font-weight:italic;font-size:18px;">Version 1.1</span></a>
				</li>
			</ul>
				<!-- END X-NAVIGATION -->
        </div>
        <!-- END PAGE SIDEBAR -->

        <!-- PAGE CONTENT -->
        <div class="page-content" style="font-size:20px;color:black">
            <!-- START X-NAVIGATION VERTICAL -->
            <ul class="x-navigation x-navigation-horizontal x-navigation-panel">
                <!-- TOGGLE NAVIGATION -->
                <li class="xn-icon-button">
                    <a href="#" class="x-navigation-minimize"><i class="fas fa-bars"></i></a>
                </li>
				<!-- END TOGGLE NAVIGATION -->
			</ul>
			
			<!-- END X-NAVIGATION VERTICAL -->
			<h1><?php echo " </br> You Have Following Error : </br></br>"; ?></h1>
