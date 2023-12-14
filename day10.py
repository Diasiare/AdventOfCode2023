import itertools
import operator
from functools import reduce

text = open("day10.txt").read()
m = list(map(list,text.splitlines()))

def n(dy1, dx1):
    return lambda y,x: (y + dy1, x + dx1) 

nexts = {
    "|": [n(1, 0), n(-1, 0)],
    "-": [n(0, 1), n(0, -1)],
    "L": [n(-1, 0), n(0, 1)],
    "J": [n(-1, 0), n(0, -1)],
    "7": [n(0, -1), n(1, 0)],
    "F": [n(1, 0), n(0, 1)],
}
cardinals = [n(0,1), n(0,-1), n(1,0), n(-1,0)]

def start(m):
    for y, row in enumerate(m):
        for x, c in enumerate(row):
            if c == 'S':
                return (y,x)

startPoint = start(m)

def connected(m, point):
    y, x = point
    shape = m[y][x]
    if not shape in nexts:
        return []
    return list(map(lambda s: s(point[0], point[1]),nexts[shape]))

def sIsType(m, startPoint):
    con = []
    for card in cardinals:
        if startPoint in connected(m, card(startPoint[0], startPoint[1])):
            con.append(card(startPoint[0], startPoint[1]))
    
    for k in nexts:
        v = nexts[k]
        if all(map(lambda x: x in con, list(map(lambda s: s(startPoint[0], startPoint[1]), v)))):
            return k

def findCycle(m, startPoint):
    con = []
    for card in cardinals:
        if startPoint in connected(m, card(startPoint[0], startPoint[1])):
            con.append(card(startPoint[0], startPoint[1]))

    n = [startPoint, con[0]]
    while not n[-1] == startPoint:
        c = n[-1]
        p = n[-2]
        next = list(filter(lambda x: not x == p, connected(m,c)))[0]
        n.append(next)
    return n
    

cycle = findCycle(m, startPoint)

print("Part 1: ", (len(cycle) - 1)// 2)

sIs = sIsType(m,startPoint)

enclosedPoint = {
    "L": n(-1, 1),
    "J": n(-1, -1),
    "7": n(1, -1),
    "F": n(1,1)
}

def t2(point):
    return (point[0] * 2, point[1]* 2) 

def nei(point):
    for card in cardinals:
        yield card(point[0],point[1])

around = [n(0,1), n(0,-1), n(1,0), n(-1,0),n(1,1), n(1,-1), n(-1,1), n(-1,-1)]

def allNei(points):
    for p in points:
        for a in around:
            yield a(p[0], p[1])


cycleSet = set()
for c in cycle:
    toAdd = t2(c)
    cycleSet.add(toAdd)
    t = m[c[0]][c[1]]
    if t == 'S':
        t = sIs
    for n in nexts[t]:
        cycleSet.add(n(toAdd[0], toAdd[1]))


notEnclosed = set()
allPoints = []
for y, row in enumerate(m):
    for x in range(len(row)):
        allPoints.append(t2((y,x)))
allTruePoints = set(allPoints)
allPoints =  set(allNei(allTruePoints)).union(allTruePoints)
front = [(-1,-1)]


while len(front)> 0:
    current = front.pop()
    if current in notEnclosed:
        continue
    notEnclosed.add(current)
    if current in cycleSet:
        continue
    for next in nei(current):
        if next in allPoints:
            front.append(next)


print("Part 2: ", len(allTruePoints - notEnclosed - cycleSet))