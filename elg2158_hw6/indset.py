#!/usr/bin/python

# Independent set problem

# sys
import sys
# Import PuLP modeler functions
from pulp import *
#Import NetworkX to read files
from networkx import *

def readG(path):
    # Read in GML graph
    G = read_gml(path)
    # Set all edge capacities to 1
    G.add_edges_from(G.edges_iter(), capacity=1)
    return G
    
def main():
    # Set up arguments
    path = sys.argv[1]

    # Set up graph
    G = readG(path)
    
    method1(G)
    method2(G)
    method3(G)

def method1(G):
    # Use networkX flow algorithm to print the size of independent set
    # method 1 on homework
    list = []
    for i in range(0,10):
    	 mis = maximal_independent_set(G)
    	 print len(mis)
    	 list.append(len(mis))
    print(max(list))
    
def method2(G):
	# Define LP problem
    myprob = LpProblem("Maximum Independent Set", LpMaximize)

    # Define x variables
    x = []
    for i in G.nodes_iter():
        # optimal x={0,1}, 1 if in graph, 0 if not. 
        xvar = LpVariable("x"+str(i), 0, 1, LpInteger)
        x.append(xvar)

    # Define constraints
    for (i,j) in G.edges_iter():
        myprob += x[i-1] + x[j-1] <= 1, "x"+str(i)+"_"+str(j)
            
    # Objective
    myprob += lpSum(x) # assume all edge weights = 1

    # Solve LP
    # print(myprob)
    myprob.solve(COIN_CMD())

    # Print optimization value
    print value(myprob.objective)    	 
   
def method3(G):
	# Define LP problem
    myprob = LpProblem("Maximum Independent Set", LpMaximize)

    # Define x variables
    x = []
    for i in G.nodes_iter():
        # optimal x={0,1}, 1 if in graph, 0 if not. 
        xvar = LpVariable("x"+str(i), 0, 1)
        x.append(xvar)

    # Define constraints
    for (i,j) in G.edges_iter():
        myprob += x[i-1] + x[j-1] <= 1, "x"+str(i)+"_"+str(j)
            
    # Objective
    myprob += lpSum(x) # assume all edge weights = 1

    # Solve LP
 	# print(myprob)
    myprob.solve()

    # Print optimization value
    print value(myprob.objective)

if __name__ == "__main__":
    main()
