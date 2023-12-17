import itertools
import operator
from functools import reduce
import heapq

text = open("day17.txt").read()
lines = text.splitlines()
city = [list(map(int, line)) for line in lines]


directions = [(-1,0), (0,-1),(1,0),(0,1)]

def nextDirs(dir, steps):
    if steps == 3:
        return [x % 4 for x in [dir - 1, dir + 1]]
    return [x % 4 for x in [dir - 1, dir ,dir + 1]]


def nextPos(position, maxPos):
    pos, dir, steps = position
    for nDir in nextDirs(dir, steps):
        inc = directions[nDir]
        nPos = (pos[0] + inc[0], pos[1] + inc[1])
        valid = all([x < m and x >=0 for x,m in zip(nPos, maxPos)])
        if valid:
            yield (nPos, nDir, steps + 1 if nDir == dir else 1)


def minSteps(city, fr, to):
    # format (cost, (point, facing, steps-since-turn))
    queue = [(0, (fr, 0, 0)), (0, (fr, 1, 0)), (0, (fr, 2, 0)), (0, (fr, 3, 0))]
    heapq.heapify(queue)

    seen = set()
    maxX = len(city[0])
    maxY = len(city)
    maxPos =  (maxY, maxX)

    while not queue[0][1][0] == to:
        cost, position = heapq.heappop(queue)
        if position in seen:
            continue
        seen.add(position)

        for n in nextPos(position, maxPos):
            if n in seen:
                continue
            pos = n[0]
            heapq.heappush(queue, (cost + city[pos[0]][pos[1]], n))            

    return queue[0][0]

print("Part 1: ", minSteps(city, (0,0), (len(city) - 1, len(city[0]) - 1)))

def nextDirsUltra(dir, steps):
    if steps < 4:
        return [dir]
    if steps == 10:
        return [x % 4 for x in [dir - 1, dir + 1]]
    return [x % 4 for x in [dir - 1, dir ,dir + 1]]


def nextPosUltra(position, maxPos):
    pos, dir, steps = position
    for nDir in nextDirsUltra(dir, steps):
        inc = directions[nDir]
        nPos = (pos[0] + inc[0], pos[1] + inc[1])
        valid = all([x < m and x >=0 for x,m in zip(nPos, maxPos)])
        if valid:
            yield (nPos, nDir, steps + 1 if nDir == dir else 1)


def minStepsUltra(city, fr, to):
    # format (cost, (point, facing, steps-since-turn))
    queue = [(0, (fr, 0, 0)), (0, (fr, 1, 0)), (0, (fr, 2, 0)), (0, (fr, 3, 0))]
    heapq.heapify(queue)

    seen = set()
    maxX = len(city[0])
    maxY = len(city)
    maxPos =  (maxY, maxX)

    while not queue[0][1][0] == to or not queue[0][1][2] > 3:
        cost, position = heapq.heappop(queue)
        if position in seen:
            continue
        seen.add(position)

        for n in nextPosUltra(position, maxPos):
            if n in seen:
                continue
            pos = n[0]
            heapq.heappush(queue, (cost + city[pos[0]][pos[1]], n))            

    return queue[0][0]


print("Part 2: ",  minStepsUltra(city, (0,0), (len(city) - 1, len(city[0]) - 1)))