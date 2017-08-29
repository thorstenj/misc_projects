<?php
require("phpsqlinfo_dbinfo.php");

// Gets data from URL parameters.
$name = $_GET['name'];
$address = $_GET['address'];
$lat = $_GET['lat'];
$lon = $_GET['lon'];
$date = $_GET['date'];

// Opens a connection to a MySQL server.
$connection=mysql_connect("localhost", $username, $password);
if (!$connection) {
  die('Not connected : ' . mysql_error());
}

// Sets the active MySQL database.
$db_selected = mysql_select_db($database, $connection);
if (!$db_selected) {
  die ('Can\'t use db : ' . mysql_error());
}

// Inserts new row with place data.
$query = sprintf("INSERT INTO hotel " .
         " (id, name, address, lat, lon, date ) " .
         " VALUES (NULL, '%s', '%s', '%s', '%s', '%s');",
         mysql_real_escape_string($name),
         mysql_real_escape_string($address),
         mysql_real_escape_string($lat),
         mysql_real_escape_string($lng),
         mysql_real_escape_string($date));

$result = mysql_query($query);

if (!$result) {
  die('Invalid query: ' . mysql_error());
}

?>