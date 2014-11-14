#!/usr/bin/env python
from collections import defaultdict
from operator import itemgetter, attrgetter
import glob
import sys

def Readfile(file):
    graph = defaultdict(list)
    with open(file,"r") as f:
        next(f)
        for line in f:
            key, value = line.strip().split()
            key = int(key)
            value = int(value)
            graph[key].append(value)
    return graph

def Readheader(file):
    with open(file,"r") as f:
        header = f.readline()
        n, m = header.strip().split()
    return n,m

def Transposegraph(graph):
    graphT = defaultdict(list)
    for key, value in graph.iteritems():
        for i in value:
            graphT[i].append(key)
    return graphT

def scc(graph):
    V = range(1,n+1)
    Vsort = range(0,len(V))
    graphT=Transposegraph(graph)          

    def search(u):
        global t
        t = t + 1
        start[u-1] = t
        explored[u-1] = 1
        if graph.get(u) != None:
            for v in graph[u]:
                if explored[v-1] == 0:
                    search(v)
        t = t + 1
        if len(finish[u]) == 0:
            finish[u].append(t)
            
        if len(finish[u]) != 0:
            del finish[u]
            finish[u].append(t)

    def dfs(graph):
        global t
        global previous
        t = 0
        previous = 0
        for u in V:
            if explored[u-1] == 0:
                search(u)

    def dfsT(graph):
        finishtimes = []
        x = finish.values()
        for i in range(0,len(finish)):
            finishtimes.append(x[i][0])
        finishtimes_sorted, Vsort = [list(y) for y in zip(*sorted(zip(finishtimes, V), key=itemgetter(0),reverse=True))] # sort in decreasing finish times
        path=[]
        for u in Vsort:
            if explored[u-1] == 0:
                x = searchT(u)
                path.append(x)
        return path

    def searchT(u):
        visitedNodes = []
        stack = [u]
        s = u
        while len(stack) > 0:
            v = stack.pop()
            explored[v-1] = 1
            if v not in visitedNodes:
                visitedNodes.append(v)
            for w in reversed(graphT[v]):
                if explored[w-1] == 0:
                    stack.append(w)
        return visitedNodes

    t = 0
    explored = [0]*n
    start = [0]*n
    finish = defaultdict(list)
    dfs(graph)

    t = 0 
    explored = [0]*n
    start = [0]*n
    sccs = dfsT(graphT)

   # print sccs
    return sccs

def output(graph,outputname): 
    s = sorted(scc(graph))
    results = defaultdict(list)
    for i in range(0,len(s)):
        s[i] = sorted(s[i])
        results[int(s[i][0])].append(s[i])
    size = str(len(s))
    with open(outputname,"w") as f:
        print >>f,size

        for x in sorted(results):
            string = str(len(results[x][0])) + ' ' + str(results[x][0])
            string = string.translate(None,',[]')
            print >>f, string
    return
        
if __name__ == "__main__":

    infiles =  glob.glob("in*.txt")
    outfiles = range(0,len(infiles))
     
    for i in range(0,len(infiles)):
        outfilename = infiles[i].translate(None,'in')
        outfilename = "out" + outfilename
        outfiles[i] = outfilename

    for i in range(0,len(infiles)):
       # if i in {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19}:
       #       continue
        print infiles[i]
        graph = Readfile(infiles[i])
        a = Readheader(infiles[i])
        global n
        n = int(a[0])
        output(graph,outfiles[i])

## stdin and stdout ???? 
