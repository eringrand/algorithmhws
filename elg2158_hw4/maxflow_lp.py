#!/usr/bin/python

# Import sys to read command line argument
import sys
# Import PuLP modeler functions to solve LP
from pulp import *
# Import NetworkX to read files
from networkx import *
# Import defaultdict to set up incoming and outgoing lists
from collections import defaultdict

def readG(path):
    G = read_gml(path)
    return G    

def main():
    path = sys.argv[1]
    s = int(sys.argv[2])
    t = int(sys.argv[3])

    G = readG(path)
    H = G.to_directed()
    incoming = defaultdict(list)
    outgoing = defaultdict(list)

    # Define LP problem
    myprob = LpProblem("Maximum Flow", LpMaximize)

    for (i,j) in H.edges_iter():
        # Make variables for the flow lines, max flow at capacity = 1
        # Make variables for both directions beacuse we need edges to go from i-j and j-i
        edgevar = LpVariable("edge_from_"+str(j)+"_to_"+str(i), 0, 1, LpInteger)
        incoming[i].append(edgevar)
        outgoing[i].append(edgevar)

    # Objective
    myprob += lpSum(incoming[s]) - lpSum(outgoing[s])

    # Constraints
    for u in G.nodes_iter():
        if u != s and u != t:
            myprob += lpSum(incoming[u]) - lpSum(outgoing[u]) == 0, "flow" + str(u)

    # Target constraint
    myprob += lpSum(incoming[t]) - lpSum(outgoing[t]) == -(lpSum(incoming[s]) - lpSum(outgoing[s])), "target flow"

    # Solve LP problem
    myprob.solve()
    
    # Print maxflow value
    print int(value(myprob.objective))

if __name__ == "__main__":
    main()
