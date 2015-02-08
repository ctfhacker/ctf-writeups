<?php
  require_once("root_data.php");
  include(STEVES_LIST_ABSOLUTE_INCLUDE_ROOT . "cookies.php");
  require_once(STEVES_LIST_ABSOLUTE_INCLUDE_ROOT . "includes/classes.php");
  // Okay, this is the front page.
  // We should just display all the recent posts. We'll figure out how to add posts later.
  $posts = array_diff(scandir(STEVES_LIST_ABSOLUTE_INCLUDE_ROOT . "posts"), array('..', '.'));
  $display_posts = array();
  if ($custom_settings[DISPLAY_POSTS]) {
    // display posts
    foreach ($posts as $p) {
      $contents = file_get_contents(STEVES_LIST_ABSOLUTE_INCLUDE_ROOT . "posts/" . $p);
      $post = unserialize($contents);
      $display_posts []= $post;
    }
  }
  require_once(STEVES_LIST_TEMPLATES_PATH . "view_posts.php");
?>
