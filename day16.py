import itertools
import operator
from functools import reduce

text = open("day16.txt").read()
lines = text.splitlines()

directions = [(-1,0), (0,-1),(1,0),(0,1)]

def isNorthSouth(d):
    return d in [0,2]
def isWestEast(d):
    return d in [1,3]

forwardslashBounce = {
 0: 3,
 1: 2,
 2: 1,
 3: 0   
}

backslashBounce = {
    0 : 1,
    1 : 0,
    2 : 3,
    3 : 2,
}



def move(map, beam, max):
    position, direction = beam
    newPos = (position[0] + directions[direction][0], position[1] + directions[direction][1])
    
    # Left the map
    for (p,pm) in zip(newPos, max):
        if p < 0 or p > pm:
            return [None]
    
    c = map[newPos[0]][newPos[1]]

    if c == "|" and isWestEast(direction):
        return [(newPos, 0), (newPos, 2)]
    if c == "-" and isNorthSouth(direction):
        return [(newPos, 1), (newPos, 3)]
    if c == "/":
        return [ (newPos, forwardslashBounce[direction])]
    if c == "\\":
        return [ (newPos, backslashBounce[direction])]    
    return [(newPos, direction)]



def energizedCount(lines, startBeam):
    beams = [startBeam]
    maxY = len(lines) - 1
    maxX = len(lines[0]) - 1
    energized = set()
    seen = set()

    while len(beams) > 0:
        nbeams = []
        for beam in beams:
            if beam in seen:
                continue
            seen.add(beam)
            nb = move(lines, beam, (maxY, maxX))
            for b in nb:
                if b == None:
                    continue
                nbeams.append(b)
                energized.add(b[0])
        beams = nbeams
    return len(energized)


dirToSign = {
    0: '^',
    1: '<',
    2: 'v',
    3: '>'
}

def visualize(map, seen):
    pointCollection = {}
    for position, direction in seen:
        if position in pointCollection:
            pointCollection[position].append(direction)
        else:
            pointCollection[position] = [direction]

    out = ""

    for i , line in enumerate(map):
        for j, c in enumerate(line):
            if not c == '.':
                out +=c
            elif (i,j) in pointCollection:
                col = pointCollection[(i,j)]
                if len(col) > 1:
                    out += str(len(col))
                else:
                    out += dirToSign[col[0]]
            else:
                out += '.'
                
        out += '\n'
    
    return out


print("Part 1: ", energizedCount(lines, ((0,-1), 3)))

mY = len(lines) 
mX = len(lines[0]) 

counts = [energizedCount(lines, ((x, -1), 3)) for x in range(mY)]
counts.extend([energizedCount(lines, ((x, mX ), 1)) for x in range(mY)])
counts.extend([energizedCount(lines, ((-1, x), 2)) for x in range(mX)])
counts.extend([energizedCount(lines, ((mY, x), 0)) for x in range(mX)])

m = max(counts)


print("Part 2: ", m)