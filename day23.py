import itertools
import operator
from functools import reduce
from queue import Queue

text = open("day23.txt").read()
lines = text.splitlines()
area = [list(line) for line in lines]

directions = [(1,0), (-1,0), (0,1), (0,-1)]
slopeDir = {
    '>': (0,1),
    '<': (0,-1),
    'v': (1, 0),
    '^': (-1,0),
}

maxX = len(area[0]) - 1
maxY = len(area) - 1

start = None
end = None
for i,c in enumerate(area[0]):
    if c == '.':
        start = (0, i)
        break
for i,c in enumerate(area[-1]):
    if c == '.':
        end = (len(area) - 1, i)
        break


def takeStep(point):
    place, seen = point

    current = area[place[0]][place[1]]
    out = []
    for dir in directions if not current in slopeDir else [slopeDir[current]]:
        newPlace = (place[0] + dir[0], place[1] + dir[1])
        y,x = newPlace
        if y < 0 or y > maxY or x < 0 or x > maxY:
            continue
        t = area[y][x] 
        if t == '#':
            continue
        if newPlace in seen:
            continue
        newSeen = set([newPlace]).union(seen)
        out.append((newPlace, newSeen))
    return out

queue = Queue()
#queue.put((start, set([start])))
found = []

while not queue.empty():
    point = queue.get()

    newPoints = takeStep(point)

    for p in newPoints:
        if p[0] == end:
            found.append(p)
        else:
            queue.put(p)

result =0# max([len(p[1]) for p in found])


print("Part 1: ", result - 1)


def getNexts(place):
    out = []
    for dir in directions:
        newPlace = (place[0] + dir[0], place[1] + dir[1])
        y,x = newPlace
        if y < 0 or y > maxY or x < 0 or x > maxY:
            continue
        t = area[y][x] 
        if t == '#':
            continue
        out.append(newPlace)
    return out


def simplify(graph):
    queue = Queue()
    queue.put(start)

    seen = set()
    while not queue.empty():
        p = queue.get()
        if p in seen:
            continue
        seen.add(p)

        for next in list(graph[p].keys()):
            while len(graph[next]) == 2:
                nextNext = [x for x in graph[next] if not x == p][0]
                newLen = graph[next][p] + graph[next][nextNext]
                del graph[next]
                del graph[p][next]
                del graph[nextNext][next]
                graph[p][nextNext] = newLen
                graph[nextNext][p] = newLen
                next = nextNext
            queue.put(next)



def toGraph():
    graph = {}
    queue = Queue()
    queue.put(start)

    while not queue.empty():
        p = queue.get()
        if p in graph:
            continue
        graph[p] = {}
        
        for np in getNexts(p):
            graph[p][np] = 1
            queue.put(np)

    simplify(graph)
    return graph


def takeStepWoSlope(place):
    place, seen = point

    out = []
    for dir in directions:
        newPlace = (place[0] + dir[0], place[1] + dir[1])
        y,x = newPlace
        if y < 0 or y > maxY or x < 0 or x > maxY:
            continue
        t = area[y][x] 
        if t == '#':
            continue
        if newPlace in seen:
            continue
        newSeen = set([newPlace]).union(seen)
        out.append((newPlace, newSeen))
    return out

graph = toGraph()
print("Gsize",len(graph))
print(start, end)
queue = []
queue.append((start, 0,set([start])))
found = []

endNext = list(graph[end].keys())[0]

print(graph)

maxSeen = 0

while len(queue) > 0:
    point, cLen, seen = queue.pop()

    for p in graph[point]:
        if p in seen:
            continue
        
        n = (p, cLen + graph[point][p], set([p]).union(seen))

        if n[0] == end:
            found.append(n)
        elif not point == endNext:
            queue.append(n)

result = max([p[1] for p in found])


print("Part 2: ", result + 1)