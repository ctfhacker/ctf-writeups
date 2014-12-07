from pwn import *
import subprocess
import re
import string

addr = 'disassemble.quals.seccon.jp'
port = 23168

archs = [
'8051',
'arc', 
'arm', 
'avr', 
'bf', 
'cr16',
'csr', 
'dalvik', 
'dcpu16', 
'ebc', 
'gb',
'h8300',
'i8080',
'java', 
'm68k', 
'malbolge', 
'mips', 
'msil', 
'msp430', 
'nios2', 
'ppc', 
'rar', 
'sh', 
'sparc', 
'spc700', 
'sysz', 
'tms320', 
'v850', 
'ws', 
'x86', 
'xcore', 
'z80', 
'psosvm', 
'propeller', 
'6502',
'x86.nasm',
'snes', 
]

for curr_arch in archs:
    with remote(addr, port) as r:
        arch = curr_arch
    
        # Grab problem
        msg = r.recv(timeout=3)
        print msg

        # Get only the assembly from problem
        asm = msg.split('\n')[0].split(':')[1].replace(' ','')

        # Call rasm2 with the assembly and correct architecture
        res = subprocess.check_output('rasm2 -d "{}" -a {}'.format(asm, arch), shell=True)
        try:
            print '{0} {1} {0}'.format('-'*20, arch)
            r.clean(1)
            r.sendline(res)
            log.info("In: {} Out: {}".format(asm, res))
            if '#2' in r.recv(timeout=2):
                print "FOUND IT"
                raw_input()
        except Exception as e:
            print str(e)
            pass
