<?php

$locDir = "/home/pi/local/www/";
$filepath= "";

if ($_SERVER["REQUEST_METHOD"] == "GET") {
	//NOTE: nothing can be output prior to the image for this to work
	//var_dump($_GET);
	//echo "WORKING!";

	// get the file name
	$filepath= $locDir . @$_GET['file'];

	if (file_exists($filepath)){
		
		//this will run php code
    	//include($filepath);

    	//this wont run any php code
    	echo file_get_contents($filepath);

	} else {
		notFound();
		//echo $filepath . " not found";
	}
	
}

function notFound(){
	echo file_get_contents("404.html");
}

?>