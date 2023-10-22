// Server Update script
// Roni Bandini @RoniBandini
// October 2023, MIT License
// Receives helmet detection % from AM62A and queries from Unihiker Traffic Light

<?php

$fichero = 'helmet.ini';

$actual=filter_var($_GET["nohelmet"], FILTER_SANITIZE_NUMBER_FLOAT,FILTER_FLAG_ALLOW_FRACTION);

file_put_contents($fichero, $actual);

echo "Server updated...";

?>
