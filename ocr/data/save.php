<?php
echo $_POST;
file_put_contents('images/data.json', file_get_contents('php://input'));

?>
