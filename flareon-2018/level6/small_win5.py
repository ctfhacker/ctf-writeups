import angr
import claripy
from reconstruct import decrypt

def hook_mem_write(state):
    if not state.inspect.instruction:
        return
    print('{:x} [{}] = {}'.format(state.inspect.instruction,
                                  state.inspect.mem_write_address, 
                                  state.inspect.mem_write_expr))

def hook_mem_read(state):
    if not state.inspect.instruction:
        return
    print('{:x} {} = [{}]'.format(state.inspect.instruction,
                                  state.inspect.mem_read_expr, 
                                  state.inspect.mem_read_address))

result = '?' * 0x45
global_addr = 0x605100

new_filename = './magic'
data = decrypt(new_filename)
import IPython; shell = IPython.terminal.embed.InteractiveShellEmbed(); shell.mainloop()
for n in xrange(33):
    # n  = 21
    proj = angr.Project('./magic_patched', load_options={"auto_load_libs": False})

    state = proj.factory.blank_state(addr=data[n].function_addr, add_options={angr.options.LAZY_SOLVES,
                                                                              angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY})
    # state.inspect.b('mem_write', when=angr.BP_AFTER, action=hook_mem_write)
    # state.inspect.b('mem_read', when=angr.BP_AFTER, action=hook_mem_read)

    input_addr = 0x10000 * n
    key_len = data[n].length

    input = claripy.BVS("input", 8*(key_len))
    for i in xrange(key_len):
        state.add_constraints(input.get_byte(i) != 0)

    state.memory.store(input_addr, input)

    key_addr = (0x605120 + n*0x120)
    state.regs.rdi = claripy.BVV(input_addr, 8*8)
    state.regs.rsi = claripy.BVV(key_len,    8*8)
    state.regs.rdx = claripy.BVV(key_addr,   8*8)
    print("Start {} - rdi: {} rsi: {} rdx: {}".format(state.regs.rip, state.regs.rdi, state.regs.rsi, state.regs.rdx))
    state.stack_push(0xdeadbeef)

    simgr = proj.factory.simulation_manager(state)

    def find_func(state):
        if state.regs.rip.args[0] == 0xdeadbeef:
            if state.regs.rax.args[0] == 1:
                global result
                try:
                    ans = state.solver.eval(input, cast_to=str)
                    print(ans)
                    print(n, repr(ans))
                    offset = data[n].offset
                    ans_len = data[n].length
                    result = result[:offset] + ans + result[offset+ans_len:]
                    print(n, result)
                    with open('status', 'a') as f:
                        f.write('{} {}\n'.format(n, result))
                    return True
                except:
                    print('ERROR: n={}'.format(n))


    def avoid_func(state):
        if state.regs.rip.args[0] == 0xdeadbeef and state.regs.rax.args[0] == 0:
            return True

    simgr.explore(find=find_func, avoid=avoid_func)
    # print(simgr)

    # print('RESULT', result)
