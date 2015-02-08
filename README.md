# Quick writeups

#### Haxdump 2015 - pwnxy
Requests a page via a given GET request. The request results is placed directly into a printf, resulting in a string format vuln. From the vuln, overwrite the `exit` entry in the GOT with a static stack address to execute code from the GET request

#### P_KR
"My first overflow" style. Simply give `0xCAFEBABE` 14 times in order to overwrite the local variable

Client/Server problem to implement a binary search in order to find a random number in a range of numbers

Input a username and two passcodes in order to "login". Using the username field, overwrite the pointer to where the first passcode writes. Use the first passcode field to overwrite the `exit` entry in the GOT with the address of the `system('/bin/sh')` provided in the binary

Input a password, it is xor'ed with a key and if it matches the password from a file, you win. Logic error in setting a file descriptor while comparing the result. Missing parentheses allowed the attacker to control both the input password and the password used to check against.

Give a base64 encoded message, and get the md5 sum of the original message. Stack canaries are on. There is a "captcha" before sending your message that is calculated with the stack canary. Random is also seeded with time(), which we also know because we have access to the server itself. Knowing this, we can calculate the calculate the stack canary ourselves. The base64 decode function allows an overflow to happen. The decoded message contains the canary at the correct location, and then a ret2system was easy peasy.


