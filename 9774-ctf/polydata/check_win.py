from tsp_solver.greedy import solve_tsp
from itertools import permutations as perm
from itertools import combinations as comb
import random
def maxsubseq(seq):
  '''Solve max subsequence sum'''
  return sum(max((seq[begin:end] for begin in xrange(len(seq)+1)
                             for end in xrange(begin, len(seq)+1)),
             key=sum))

"""
Unbounded Knapsack
def knapsack(items, C):
    '''Solve 0/1 knapsack'''
    NAME, SIZE, VALUE = range(3)
    # order by max value per item size
    # for item in items:
        # print '[{}] V: {} S: {}'.format(item, item[VALUE], item[SIZE])
    items = sorted(items, key=lambda item: item[VALUE]/float(item[SIZE]), reverse=True)
 
    # Sack keeps track of max value so far as well as the count of each item in the sack
    sack = [(0, [0 for i in items]) for i in range(0, C+1)]   # value, [item counts]
 
    for i,item in enumerate(items):
        name, size, value = item
        for c in range(size, C+1):
            sackwithout = sack[c-size]  # previous max sack to try adding this item to
            trial = sackwithout[0] + value
            used = sackwithout[1][i]
            if sack[c][0] < trial:
                # old max sack with this added item is better
                sack[c] = (trial, sackwithout[1][:])
                sack[c][1][i] +=1   # use one more
 
    value, bagged = sack[C]
    numbagged = sum(bagged)
    size = sum(items[i][1]*n for i,n in enumerate(bagged))
    # convert to (iten, count) pairs) in name order
    bagged = sorted((items[i][NAME], n) for i,n in enumerate(bagged) if n)
 
    return value, size, numbagged, bagged
"""

def totalvalue(comb):
    ' Totalise a particular combination of items'
    totwt = totval = 0
    for item, wt, val in comb:
        totwt  += wt
        totval += val
    return (totval, -totwt) if totwt <= 400 else (0, 0)
 
def knapsack(items, limit):
    table = [[0 for w in range(limit + 1)] for j in xrange(len(items) + 1)]
 
    for j in xrange(1, len(items) + 1):
        item, wt, val = items[j-1]
        for w in xrange(1, limit + 1):
            if wt > w:
                table[j][w] = table[j-1][w]
            else:
                table[j][w] = max(table[j-1][w],
                                  table[j-1][w-wt] + val)
 
    result = []
    w = limit
    for j in range(len(items), 0, -1):
        was_added = table[j][w] != table[j-1][w]
 
        if was_added:
            item, wt, val = items[j-1]
            result.append(items[j-1])
            w -= wt
 
    return result
 
 

def create_graph(seq):
    '''Utility function to create the matrix for tsp_solver'''
    # Make the graph 0 indexed, not 1 indexed for tsp_solver
    curr_seq = seq[:]
    for index,num in enumerate(curr_seq):
        if index%3 != 2:
            curr_seq[index] = curr_seq[index]-1
    num_nodes = len(curr_seq) / 3
    graph = [[999]*num_nodes for _ in xrange(num_nodes)]
    nodes = [curr_seq[x:x+3] for x in xrange(0,len(curr_seq),3)]
    for n1, n2, weight in nodes:
        graph[n1][n2] = weight
        graph[n2][n1] = weight
    return graph

def init_knapsack(seq):
    '''Convert our sequence into input for the knapsack solver'''
    capacity = seq[0]
    items = [seq[x:x+2] for x in xrange(1, len(seq), 2)]
    items = [(chr(index+0x41), item[0], item[1]) for index, item in enumerate(items)]
    return capacity, items

def path_to_weight(path, graph):
    '''Sum the weights of the TSP path'''
    edges = [path[x:x+2] for x in xrange(len(path)-1)]
    return sum(graph[n1][n2] for n1,n2 in edges)

def answer_knapsack(seq):
    '''Top level function for knapsack'''
    # bagged = knapsack(items, 400)
    # val, wt = totalvalue(bagged)

    capacity, items = init_knapsack(seq)
    return knapsack(items, capacity)[0][2]

def answer_tsp(seq):
    '''Top level function for TSP'''
    graph = create_graph(seq)
    path = solve_tsp(graph)
    return path_to_weight(path, graph)

"""
Knowledge:
Knapsack weights must be positive, which means every even number
in the sequence must be positive.

Only odd sequences where len(seq) % 3 == 0 can be used, because
Knapsack requires odd number sequences (Capacity + 2*) and TSP
requires sequences to be mod % 3 == 0

Sequence of 9:
     [1,  2,  3,  3,  1,  1,  2,  3,  1]
Knap  Cap V1  W1  V2  W2  V3  W3  V4  W4
TSP   N1  N2  WeigN3  N1  WeigN2  N3  Weig
"""

def get_edges(node_count):
    nums = [0]*20
    for index, num in enumerate(nums):
        if node_count == (index+1):
            return index+num
        nums[index+1] = index+num
    
lowest = 9999
lowest_str = ''
nodes = 5
'''
while True:
    for nodes in xrange(5, 10):
        for num_edges in xrange(get_edges(nodes)):
            for edges in perm(perm(xrange(1, nodes+1), 2), num_edges):
                while True:
                    curr_seq = []
                    curr_rand = 0
                    
                    for index,edge in enumerate(edges):
                        curr_seq += list(edge)
                        curr_rand = random.randint(-100, 100)
                        curr_seq.append(curr_rand)

                    if [x for x in curr_seq[1::2] if x <= 0]:
                        continue
                    break

                edges = [tuple(curr_seq[x:x+2]) for x in xrange(len(curr_seq)) if x % 3 == 0]

                # Ensure we don't have double edges in our sequence
                bad = False
                for n1, n2 in edges:
                    if (n2, n1) in edges:
                        bad = True
                if bad:
                    continue

                try:
'''
for num5 in xrange(-20, 20):
    for num1 in xrange(-20, 20):
        for num2 in xrange(-20, 20):
            for num3 in xrange(-20, 20):
                for num4 in xrange(-20, 20):
                    try:
                        # print "{} {} {} {} {}".format(num1, num2, num3, num4, num5)
                        curr_seq = [1, 3, num1, 2, 3, num2, 4, 1, num5, 1, 5, num3, 2, 4, num4] 
                        knapsack_ans = answer_knapsack(curr_seq)
                        maxsub_ans = maxsubseq(curr_seq)
                        tsp_ans = answer_tsp(curr_seq)
                        delta = max(maxsub_ans, tsp_ans, knapsack_ans)\
                               - min(maxsub_ans, tsp_ans, knapsack_ans)
                        if delta < lowest:
                            print "{} TSP: {} KS: {} MS: {}\n{}".format(str(curr_seq).replace('[','').replace(']','').replace(',', ' '), tsp_ans, knapsack_ans, maxsub_ans, curr_seq)
                            lowest = delta
                            lowest_str = "{} TSP: {} KS: {} MS: {}".format(curr_seq, tsp_ans, knapsack_ans, maxsub_ans)
                        if tsp_ans == knapsack_ans == maxsub_ans:
                            raw_input("FOUND IT")
                    except IndexError:
                        pass
                 
'''
                except IndexError:
                    continue
'''
                
