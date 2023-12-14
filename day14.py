import itertools
import operator
from functools import reduce

text = open("day14.txt").read()
table = list(map(list,text.splitlines()))


def getOrNone(table, y, x):
    if  y >= len(table) or y < 0:
        return None
    row = table[y]
    if x >= len(row) or x < 0:
        return None
    return row[x]

def slide(table, y,x,next):
    if table[y][x] in ['.', '#']:
        return table
    ny, nx = next(y,x)
    while getOrNone(table, ny, nx) == '.':
        table[y][x] = '.'
        table[ny][nx] = 'O'
        x, y = (nx, ny)
        ny, nx = next(y,x)

    return table

def load(table):
    rows = len(table)

    score = 0
    for y, row in enumerate(table):
        for c in row:
            if c == 'O':
                score += rows - y
    return score

def nw(table):
    for y, row in enumerate(table):
        for x in range(len(row)):
            yield (y,x)

def se(table):
    for y in range(len(table) - 1, -1, -1):
        row = table[y]
        for x in range(len(row) - 1, -1 , -1):
            yield (y,x)

def rollAll(table, next, steps):
    for y,x in steps:
        slide(table, y, x, next) 

rollAll(table, lambda y,x : (y - 1, x), nw(table))

print("Part 1: ", load(table))

table = list(map(list,text.splitlines()))
cycle = [lambda y,x : (y - 1, x), lambda y,x : (y, x - 1), lambda y,x : (y + 1, x), lambda y,x : (y , x + 1)]
it = [nw, nw, se, se]

seen = {}

i = 0

def toString(table):
    out = ""
    for row in table:
        for c in row:
            out += c
        out += '\n'
    return out

target = 1000000000

while i < 1000000000 and not str(table) in seen:
    seen[str(table)] = i
    for c, d in zip(cycle, it):
        rollAll(table, c, d(table))
    i += 1

firstLoop = i
loopStart = seen[str(table)]
diff = firstLoop - loopStart
rem = target - firstLoop

toDo = rem % diff
for i in range(toDo):
    for c, d in zip(cycle, it):
        rollAll(table, c, d(table))
    
print("Part 2:", load(table))