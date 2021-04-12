<?php

#comment out these lines for production version
/*ini_set('display_errors', 1); 
ini_set('display_startup_errors', 1); 
error_reporting(E_ALL);*/

$servername = "localhost";

// 
// If you change this value, the client keys need to match
//$api_key_value = "tPmAT5Ab3j7F9";//remove this once hash is tested
$hash = '$2y$10$mCxhv3NC4/lkSycnD85XLuw/AYBCxw1ElmCqeksR.f88BTZoXXuca';
//$api_key_value = getenv('SP_API_KEY'); //THIS LINE HASN'T BEEN TESTED - remove this assuming hash works...

$api_key= $stamp = $ip = $mac = $name = "";
$log = [];

//$ccDir = "/home/pi/solar-protocol/charge-controller/data/";

if ($_SERVER["REQUEST_METHOD"] == "POST") {

  $fileName = "/home/pi/solar-protocol/backend/api/v1/deviceList.json";

  $api_key = test_input($_POST["api_key"]);

  //check if key is correct
  if(verifyPW($api_key, $hash)) {

    //set variables to POST
    $stamp = test_input($_POST["stamp"]);
    $ip = test_input($_POST["ip"]);
    $mac = test_input($_POST["mac"]);
    $name = test_input($_POST["name"]);
    $log = explode(',',test_input($_POST["log"]));
    var_dump($log);

    // Read the file contents into a string variable,
    // and parse the string into a data structure
    $str_data = file_get_contents($fileName);
    $data = json_decode($str_data,true);
    
    //var_dump($data);

    $newEntry = [];

    //check if any content exists
    if (is_null($data)){
        $data = [[
          "mac" => $mac,
          "ip" => $ip,
          "time stamp" => $stamp,
          "name" => $name,
          "log" => $log
        ]];
    } else {
      //loop through to check if entry with mac address exists
      $newMac = true;
      for ($i = 0; $i < sizeof($data);$i++){
        if($data[$i]['mac']==$mac){
            $data[$i]['ip']= $ip;
            $data[$i]['time stamp']= $stamp;
            $data[$i]['name']= $name;
            $data[$i]['log']=$log;
            $newMac = false;
            break;
        }
      }
      //create a new entry if needed
      if ($newMac == true){
        $newEntry = [
          "mac" => $mac,
          "ip" => $ip,
          "time stamp" => $stamp,
          "name" => $name,
          "log" => $log
        ];
        array_push($data, $newEntry);
      }

      var_dump($data);
    }

    $fp = fopen($fileName, 'w') or die("Error opening output file");
    fwrite($fp, json_encode($data));
    fclose($fp);
  }
  else {
    echo "Wrong API Key provided.";
  }
}

function verifyPW($pw, $hash){

# hash generated from password_hash() more info at https://www.php.net/manual/en/function.password-hash.php

  if(password_verify($pw, $hash)){
    return true;
  }
  return false;
}

function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}
/*
function chargeControllerData(){
  $fileDate = date("Y-m-d");
  $fileName = "/home/pi/solar-protocol/charge-controller/data/tracerData" . $fileDate . ".csv";
    
  $rawDataArray = [];

  if (($h = fopen("{$fileName}", "r")) !== FALSE) {
    // Each line in the file is converted into an individual array that we call $data
    // The items of the array are comma separated
    while (($data = fgetcsv($h, 1000, ",")) !== FALSE) 
    {
      // Each individual array is being pushed into the nested array
      $rawDataArray[] = $data;        
    }

    // Close the file
    fclose($h);

    return $rawDataArray;
  } else {
    return FALSE;
  }
}*/

function getFile($fileName){
  //echo $fileName;
  try{
    return file_get_contents($fileName);
  }
  catch(Exception $e) {
    echo $fileName;
    return FALSE;
  }

}