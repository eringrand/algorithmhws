#!/usr/bin/python

# in LP make sure you account for both ways
# LP has to take less than 35 seconds to run

# sys
import sys
# Import PuLP modeler functions
from pulp import *
#Import NetworkX to read files
from networkx import *
#Important collection to make dictionaries
from collections import defaultdict

def readG(path):
    G = read_gml(path)
    # Include both directions beacuse we need edges to go from i-j and j-i
    H = G.to_directed()
    return H 

def main():
    path = sys.argv[1]
    s = int(sys.argv[2])
    t = int(sys.argv[3])

    H = readG(path)
    q = []
    p = []

    # Define LP problem
    myprob = LpProblem("Minimum Cut", LpMinimize)

    # Define p variables
    for i in H.nodes_iter():
        # optimal when p_i = 0 if i in S, and p_i = 1 if i in T
        pvar = LpVariable("p"+str(i), 0, 1, LpInteger)
        p.append(pvar)

    # Define q variables and constraints
    for (i,j) in H.edges_iter():
        if i == s and j == t:
            qvar = LpVariable("q"+str(s)+"_"+str(t), 0, 1, LpInteger)
            myprob += qvar == 1, "q"+str(s)+"_"+str(t)
        else:
            qvar = LpVariable("q"+str(i)+"_"+str(j), 0, 1, LpInteger)
            myprob += p[j-1] - p[i-1] <= qvar, "p"+str(i)+"_"+str(j)
        q.append(qvar)

    # Set up source and target optimimum constraints
    myprob += p[t-1] - p[s-1] == 1, "def"+str(s)+"_"+str(t)
    myprob += p[t-1] == 1, "sinks"+str(s)+"_"+str(t)
    myprob += p[s-1] == 0, "sources"+str(s)+"_"+str(t)
            
    # Objective
    myprob += lpSum(q) # assume all c_ij = 1

    # Solve LP
    myprob.solve()

    # Print mincut value
    print int(value(myprob.objective))

if __name__ == "__main__":
    main()
