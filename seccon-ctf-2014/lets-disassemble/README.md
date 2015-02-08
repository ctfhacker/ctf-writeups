# Lets Dissemble

We are given a service that returns hex bytes that are assembly instructions.
Our job is to create a client to respond with the correct instruction
cooresponding to the given assembly.

What language do we disassemble to, you might ask? Let's ask radare!

## Finding the given language

I used [radare](http://github.com/radare/radare2) for this task. Radare is a multi-architecture and multi-platform command line reverse engineering toolkit. One tool in the tool box is `rasm2` which can take hex digits and convert them into the cooresponding assembly instruction. 

I looked at the supported languages via `rasm2 -L`

```bash
$ rasm2 -L
_dA_  8          8051        PD      8051 Intel CPU
_dA_  16 32      arc         GPL3    Argonaut RISC Core
_dAe  16 32 64   arm         BSD     Capstone ARM disassembler
adA_  16 32 64   arm.gnu     GPL3    Acorn RISC Machine CPU
_d__  16 32      arm.winedbg LGPL2   WineDBG's ARM disassembler
_dA_  16 32      avr         GPL     AVR Atmel
adAe  16 32      bf          LGPL3   Brainfuck
_dA_  16         cr16        LGPL3   cr16 disassembly plugin
_dA_  16         csr         PD      Cambridge Silicon Radio (CSR)
adA_  32 64      dalvik      LGPL3   AndroidVM Dalvik
ad__  16         dcpu16      PD      Mojang's DCPU-16
_dA_  32 64      ebc         LGPL3   EFI Bytecode
_dAe  8          gb          LGPL3   GameBoy(TM) (z80-like)
_dA_  16         h8300       LGPL3   H8/300 disassembly plugin
_d__             i4004       LGPL3   Intel 4004 microprocessor
_dA_  8          i8080       BSD     Intel 8080 CPU
adA_  32         java        Apache  Java bytecode
_dA_  16 32      m68k        BSD     Motorola 68000
_dA_  32         malbolge    LGPL3   Malbolge Ternary VM
adAe  16 32 64   mips        BSD     Capstone MIPS disassembler
adAe  32 64      mips.gnu    GPL3    MIPS CPU
_d__  16 32 64   msil        PD      .NET Microsoft Intermediate Language
_dA_  16         msp430      LGPL3   msp430 disassembly plugin
_dAe  32         nios2       GPL3    NIOS II Embedded Processor
_dA_  32 64      ppc         BSD     Capstone PowerPC disassembler
_dA_  32 64      ppc.gnu     GPL3    PowerPC
ad__             rar         LGPL3   RAR VM
_dA_  32         sh          GPL3    SuperH-4 CPU
_dAe  32 64      sparc       BSD     Capstone SPARC disassembler
_dA_  32 64      sparc.gnu   GPL3    Scalable Processor Architecture
_d__  16         spc700      LGPL3   spc700, snes' sound-chip
_d__  32         sysz        BSD     SystemZ CPU disassembler
_dA_  32         tms320      LGPLv3  TMS320 DSP family
_dA_  32         v850        LGPL3   v850 disassembly plugin
_dA_  32         ws          LGPL3   Whitespace esotheric VM
_dAe  16 32 64   x86         BSD     Capstone X86 disassembler
a___  32 64      x86.nz      LGPL3   x86 handmade assembler
ad__  32         x86.olly    GPL2    OllyDBG X86 disassembler
_dAe  16 32 64   x86.udis    BSD     udis86 x86-16,32,64
_dAe  32         xcore       BSD     Capstone XCore disassembler
adA_  8          z80         NC-GPL2 Zilog Z80
ad__  8 16       psosvm      BSD     Smartcard PSOS Virtual Machine
_d__  32         propeller   LGPL3   propeller disassembly plugin
_d__  8 16       6502        LGPL3   6502/NES/C64/T-1000 CPU
a___  16 32 64   x86.nasm    LGPL3   X86 nasm assembler
_d__  8 16       snes        LGPL3   SuperNES CPU
a___  16 32 64   x86.as      LGPL3   Intel X86 GNU Assembler
```

By simply looped through this list sending back a response to the server until I received a second question. My initial assumption was that the server is single architecture, so once I found one successful answer, the rest should be easy-peasy.

See [find_language.py](https://github.com/thebarbershopper/ctf-writeups/blob/master/seccon-ctf-2014/lets-disassemble/find_language.py) 

The script stopped at language `z80`. 

```bash
$ rasm2 -d AC -a z80
xor h
```

Using this language moving forward, there was one more small bug to iron out before getting the golden flag.

`rasm2` spit out a few commands where the offset arithmetic was adding a negative number instead of simply subtracting the correct value. The server wasn't too happy about this. The solution was to simply calculate the negative value and replace the offset with the correct subtraction.


After solving 100 problems:
```bash
[*] In: CB23 Out: sla e
[*] In: 85 Out: add a, l
[*] In: EDA9 Out: cpd
[*] In: DDCBAF7E Out: bit 7, (ix-81)
The flag is SECCON{I love Z80. How about you?}
```
