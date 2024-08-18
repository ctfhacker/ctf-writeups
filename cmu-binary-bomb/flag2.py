## Full writeup found on http://www.ctfhacker.com
## Binary found here: http://csapp.cs.cmu.edu/3e/bomb.tar

import angr
import logging
import claripy

def main():
    proj = angr.Project('bomb', auto_load_libs=False)

    logging.basicConfig()
    logging.getLogger('angr.surveyors.explorer').setLevel(logging.DEBUG)

    bomb_explode = 0x40143a

    # Start analysis at the phase_2 function after the sscanf
    state = proj.factory.blank_state(addr=0x400f0a)

    # Sscanf is looking for '%d %d %d %d %d %d' which ends up dropping 6 ints onto the stack
    # We will create 6 symbolic values onto the stack to mimic this 
    for i in range(6):
        state.memory.store(state.regs.rsp + i * 4, state.solver.BVS(f'int{i}', 32))

    # Attempt to find a path to the end of the phase_2 function while avoiding the bomb_explode
    ex = proj.factory.simulation_manager(state)
    ex.explore(find=0x400f3c, avoid=bomb_explode)

    if ex.found:
        found = ex.found[0]
    
        answer = []

        for _ in range(3):
            curr_int = found.solver.eval(found.stack_pop())

            # We are popping off 8 bytes at a time
            # 0x0000000200000001
            
            # This is just one way to extract the individual numbers from this popped value
            answer.append(str(curr_int & 0xffffffff))
            answer.append(str(curr_int>>32 & 0xffffffff))

        return ' '.join(answer)

def test():
    assert main() == '1 2 4 8 16 32'

if __name__ == '__main__':
    print(main())
