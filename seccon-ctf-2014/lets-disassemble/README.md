# Lets Dissemble

We are given a service that returns hex bytes that are assembly instructions.
Our job is to create a client to respond with the correct instruction
cooresponding to the given assembly.

What language do we disassemble to, you might ask? Let's ask radare!

## Finding the given language

I used [radare](http://github.com/radare/radare2)


```bash
[*] In: CB23 Out: sla e
[*] In: 85 Out: add a, l
[*] In: EDA9 Out: cpd
[*] In: DDCBAF7E Out: bit 7, (ix-81)
The flag is SECCON{I love Z80. How about you?}
```
