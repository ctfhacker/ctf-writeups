from binaryninja import *
from collections import namedtuple
import sys

Struct = namedtuple('Struct', ['function_addr', 'offset', 'length'])

def decrypt(filename):
    bv = BinaryViewType.get_view_of_file(filename)
    print(bv)
    # bv.add_analysis_option("linearsweep")
    # bv.update_analysis_and_wait()

    code_addr = 0x605100
    len_addr = 0x605108
    key_addr = 0x605118

    data = []

    for x in range(33):
        curr_len = struct.unpack('<I', bv.read(len_addr, 4))[0]
        curr_code = struct.unpack('<I', bv.read(code_addr, 4))[0]
        curr_key = struct.unpack('<I', bv.read(key_addr, 4))[0]

        # print(hex(curr_code))
        # print(hex(code_addr))
        curr_struct = [x for x in struct.unpack('<QIII', bv.read(code_addr, 4 * 5))]
        data.append(Struct(curr_struct[0], curr_struct[2], curr_struct[3]))

        for i, (code, key) in enumerate(zip(bv.read(curr_code, curr_len), bv.read(curr_key, curr_len))):
            curr_char = chr(ord(code) ^ ord(key))
            bv.write(curr_code + i, curr_char)

        code_addr += 288
        len_addr += 288
        key_addr += 288

    bv.save('./magic_patched')

    return data
