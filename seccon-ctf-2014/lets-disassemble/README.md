# Lets Dissemble

We are given a service that returns hex bytes that are assembly instructions.
Our job is to create a client to respond with the correct instruction
cooresponding to the given assembly.

What language do we disassemble to, you might ask? Let's ask radare!

## Finding the given language

I used [radare](http://github.com/radare/radare2) for this task. Radare is a multi-architecture and multi-platform command line reverse engineering toolkit. One tool in the tool box is `rasm2` which can take hex digits and convert them into the cooresponding assembly instruction. 
After looking at the supported languages via `rasm2 -L`, I simply looped through this list sending back a response to the server until I received a second question. My initial assumption was that the server is single architecture, so once I found one successful answer, the rest should be easy-peasy.
See [find_language.py](https://github.com/thebarbershopper/ctf-writeups/blob/master/seccon-ctf-2014/lets-disassemble/find_language.py) 
The script stopped at language `z80`. 
Using this language moving forward, there was one more small bug to iron out before getting the golden flag.
`rasm2` spit out a few commands where the offset arithmetic was adding a negative number instead of simply subtracting the correct value. The server wasn't too happy about this. The solution was to simply calculate the negative value and replace the offset with the correct subtraction.
After solving 100 problems:
```bash
[*] In: CB23 Out: sla e
[*] In: 85 Out: add a, l
[*] In: EDA9 Out: cpd
[*] In: DDCBAF7E Out: bit 7, (ix-81)
The flag is SECCON{I love Z80. How about you?}
```
