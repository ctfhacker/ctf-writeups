#!/usr/bin/env python2
import sys
from pwn import *

elf = ELF('moneygame')
# NOP out annoying print that clears screen
elf.asm(0x80487b3, 'nop')
elf.asm(0x80487b4, 'nop')
elf.asm(0x80487b5, 'nop')
elf.asm(0x80487b6, 'nop')
elf.asm(0x80487b7, 'nop')

elf.save('moneygame-patched')
