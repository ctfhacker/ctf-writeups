from tsp_solver.greedy import solve_tsp

#Prepare the square symmetric distance matrix for 3 nodes:
#  Distance from 0 to 1 is 1.0
#                1 to 2 is 3.0
#                0 to 2 is 2.0
D = [[ 0, 1.0, 2.0],
     [ 1.0, 0, 3.0],
     [ 2.0, 3.0, 0]]

path = solve_tsp( D )

# will print [1,0,2], path with total length of 3.0 units
print path
