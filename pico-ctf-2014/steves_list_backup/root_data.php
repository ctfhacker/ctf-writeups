<?php
  define('STEVES_LIST_ABSOLUTE_INCLUDE_ROOT', dirname(__FILE__) . "/");
  define('STEVES_LIST_TEMPLATES_PATH', dirname(__FILE__) . "/templates/");
  define('DISPLAY_POSTS', 0);
  // Daedalus changed this... I guess AAAAAAAA was not a good secret :(
  define('AUTH_SECRET', "AAAAAAAA");
  require_once(STEVES_LIST_ABSOLUTE_INCLUDE_ROOT . "includes/classes.php");
?>
