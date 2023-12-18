import itertools
import operator
from functools import reduce

text = open("day18.txt").read()
lines = text.splitlines()

def parseLine(line):
    direction, length, _ = line.split()
    length = int(length)
    return (direction, length)

dirToInc = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}

def walkPath(commands):
    segments = []
    pos = (0,0)

    for direction, count in commands:
        inc = dirToInc[direction]
        start = pos
        end = (pos[0] + inc[0] * count, pos[1] + inc[1] * count)
        pos = end
        segments.append((start, end, direction))
    return segments

commands = [parseLine(x) for x in lines]
path = walkPath(commands)

def addVolume(startX, endX, startY, endY, s, c):
    return
    for y in range(startY, endY + 1):
        for x in range(startX, endX + 1):
            s[(y, x)] = c

seen = {}

# (xStart, xEnd, ystart, yEnd, should invert)
def toLines(segments):
    out = []
    volume = 0
    for  i,part in enumerate(segments):
        start, end, _ = part
        if start[0] == end[0]:
            volume += abs(start[1] - end[1]) + 1
            before = segments[i - 1]
            after = segments[(i + 1) % len(segments)]
            out.append((min(start[1], end[1]), max(start[1], end[1]) , end[0], end[0], before[2] == after[2]))
        else:
            xValue = min(start[1], end[1])
            yValues = [start[0], end[0]]
            yValues.sort()

            out.append((xValue, xValue, yValues[0] + 1, yValues[1] - 1, True))
            volume += yValues[1] - yValues[0] - 1 
    out.sort()
    for startX, endX, yStart, yEnd, _ in out:
        addVolume(startX, endX, yStart, yEnd, seen, '#')
    return (out, volume)

def segmentLineByLine(line1, line2):
    s1, e1 = line1
    s2, e2 = line2
    if e1 < s2:
        return None
    if e2 < s1:
        return None
    
    segments = []
    if s1 < s2:
        segments.append((s1, s2 - 1))
        s1 = s2
    if e1 > e2:
        segments.append((e2 + 1, e1))
        e1 = e2
    
    return ((s1, e1), segments)

def calcVolume(segments):
    lines, volume = toLines(segments)
    minX = lines[0][0]
    minY = min([x[2] for x in lines])
    maxY = max([x[3] for x in lines])
    # ((yStart, yEnd), x for previous, isInside)
    startLine = ((minY, maxY), minX - 1, False)
    trackingLines = [startLine]

    for vline in lines:
        newLines = []
        for line in trackingLines:
            band, startX, inside = line
            segments = segmentLineByLine(band, (vline[2], vline[3]))
            if segments == None:
                newLines.append(line)
            else:
                hit, rest = segments
                for r in rest:
                    newLines.append((r, startX, inside))
                newLines.append((hit, vline[1], not inside if vline[4] else inside))
                if inside:
                    length = hit[1] - hit[0] + 1
                    width =  vline[0] - startX - 1
                    volume += length * width
                    addVolume(startX + 1, vline[0] - 1, hit[0], hit[1], seen, 'O')


        trackingLines = newLines
    return volume


def toString(path):
    xs = [x[1] for x in path]
    ys = [x[0] for x in path]
    
    out = ""
    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            if (y,x) in path:
                out+= path[(y,x)]
            else:
                out+= "."
        out += "\n"
    return out
volume = calcVolume(path)

print("Part 1: ", volume)

dirToDir = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}

def parseLineFromHex(line):
    _, _, code = line.split()
    code  = code.removeprefix('(#').removesuffix(')')
    length = code[:-1]
    length = int(length, base=16)
    direction = dirToDir[code[-1]]

    return (direction, length)

commands = [parseLineFromHex(line) for line in lines]
path = walkPath(commands)

print("Part 2: ", calcVolume(path))