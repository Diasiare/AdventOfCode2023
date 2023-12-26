import itertools
import operator
from functools import reduce
from queue import Queue

text = open("day25.txt").read()
lines = text.splitlines()

def getEdges(line):
    name, edges = line.split(": ")
    out = []
    for edge in edges.split():
        out.extend([(name, edge), (edge, name)])
    return out

edges = set()
for line in lines:
    edges.update(getEdges(line))

graph = {}
for f,t in edges:
    if not f in graph:
        graph[f] = []
    graph[f].append(t)

def findPath(f, to, removedEdges):
    reached = set()
    queue = Queue()
    queue.put((f, [f]))

    while not queue.empty():
        node, path = queue.get()
        if node == to:
            return path

        if node in reached:
            continue
        reached.add(node)
        
        for next in graph[node]:
            if (node, next) in removedEdges:
                continue
            nPath = list(path)
            nPath.append(next)
            queue.put((next, nPath))
    return None

def findToRemove():
    tried = set()
    for edge in edges:
        print(len(tried)//2)
        if edge in tried:
            continue

        f,t = edge
        removedSet = set()
        removedSet.add(edge)
        removedSet.add((t, f))
        tried.update(removedSet)
        path1 = findPath(f,t, removedSet)
        for f2,t2 in zip(path1[:-1], path1[1:]):
            removedSet2 = set([(f2,t2), (t2,f2)])
            path2 = findPath(f,t, removedSet.union(removedSet2))

            for f3, t3 in zip(path2[:-1], path2[1:]):
                removedSet3 = set([(f3,t3), (t3,f3)])
                p3 = findPath(f,t, removedSet.union(removedSet2).union(removedSet3))
                if p3 == None:
                    return removedSet.union(removedSet2).union(removedSet3)
            

def reachableFrom(f, toRemove):
    reached = set()
    path = [f]
    while len(path) > 0:
        node = path.pop()
        if node in reached:
            continue
        reached.add(node)

        for next in graph[node]:
            if (node, next) in toRemove:
                continue
            path.append(next)
    return reached


print(len(edges)//2)
toRemove = findToRemove()
a,b = list(toRemove)[0]

ar = reachableFrom(a, toRemove)
br = reachableFrom(b, toRemove)


print("Part 1: ", len(ar) * len(br))


print("Part 2: ", "incomplete")