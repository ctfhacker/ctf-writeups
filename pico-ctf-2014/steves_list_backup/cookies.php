<?php
  if (isset($_COOKIE['custom_settings'])) {
    // We should verify to make sure this thing is legit.
    $custom_settings = urldecode($_COOKIE['custom_settings']);
    $hash = sha1(AUTH_SECRET . $custom_settings);
    if ($hash !== $_COOKIE['custom_settings_hash']) {
      die("Why would you hack Section Chief Steve's site? :(");
    }
    // we only support one setting for now, but we might as well put this in.
    $settings_array = explode("\n", $custom_settings);
    $custom_settings = array();
    for ($i = 0; $i < count($settings_array); $i++) {
      $setting = $settings_array[$i];
      $setting = unserialize($setting);
      $custom_settings[] = $setting;
    }
  } else {
    $custom_settings = array(0 => true);
    setcookie('custom_settings', urlencode(serialize(true)), time() + 86400 * 30, "/");
    setcookie('custom_settings_hash', sha1(AUTH_SECRET . serialize(true)), time() + 86400 * 30, "/");
  }
?>
