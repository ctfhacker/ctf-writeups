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
        while True:
            arch = 'z80'
        
            # Grab problem
            msg = r.recv(timeout=3)
            if 'Congra' in msg:
                print r.recv(timeout=3)

            # Get only the assembly from problem
            asm = msg.split('\n')[0].split(':')[1].replace(' ','')
            # Call rasm2 with the assembly and correct architecture
            res = subprocess.check_output('rasm2 -d "{}" -a {}'.format(asm, arch), shell=True)

            """
            There was a problem with signed offsets in rasm that the servers didn't enjoy.
            The solution was to get the cooresponding negative number and subtract that
            instead of adding a positive numher
            """
            m = re.search(r'\+(0x[89abcdefABCDEF].)', res)
            if m:
                # res = subprocess.check_output('rasm2 -d "{}" -a {}'.format(asm, arch), shell=True)
                offset = int(m.group(1), 16)
                signed_offset = str(~(offset-257))
                offset = '0x{}'.format(str(hex(offset))[2:4].upper())
                # signed_offset = '0x{}'.format(str(hex(signed_offset))[2:4].upper()).replace('X','')
                res = res.replace('+' + offset, '-' + signed_offset)
                res = re.sub(r'a, ','',res)
                res = re.sub(r', ([{}])'.format(string.letters),r',\1',res)
            try:
                r.clean(1)
                r.sendline(res)
                log.info("In: {} Out: {}".format(asm, res))
            except Exception as e:
                print str(e)
                break
                pass
