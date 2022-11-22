<?php
echo $_POST;
file_put_contents('salvataggio.json', file_get_contents('php://input'));

?>