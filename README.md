# Quick writeups

## Haxdump 2015 - pwnxy

Requests a page via a given GET request. The request results is placed directly into a printf, resulting in a string format vuln. From the vuln, overwrite the `exit` entry in the GOT with a static stack address to execute code from the GET request

