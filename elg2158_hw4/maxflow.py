#!/usr/bin/python

# Maxflow flow problem


from networkx import *
import sys

def readG(path):
    # Read in GML graph
    G = read_gml(path)
    # Set all edge capacities to 1
    G.add_edges_from(G.edges_iter(), capacity=1)
    return G

def main():
    # Set up arguments
    path = sys.argv[1]
    s = int(sys.argv[2])
    t = int(sys.argv[3])

    # Set up graph
    G = readG(path)
    
    # Use networkX flow algorithm to print maxflow value
    print maximum_flow_value(G,s,t)

if __name__ == "__main__":
    main()
