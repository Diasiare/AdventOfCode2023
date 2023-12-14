import itertools
import operator
from functools import reduce

text = open("day11.txt").read()
image = list(map(list,text.splitlines()))

def findGalaxies(image):
    for y, row in enumerate(image):
        for x , c in enumerate(row):
            if c == '#':
                yield y , x
             
def expand(image):
    galaxies = list(findGalaxies(image))
    gx = set(map(lambda x: x[1], galaxies))
    gy = set(map(lambda x: x[0], galaxies))

    finalWidth = len(image[0]) + len(image[0]) - len(gx)
    out = []
    for y, row in enumerate(image):
        if not y in gy:
            out.append(['.']* finalWidth)
            out.append(['.']* finalWidth)
            continue
        
        nr = []
        for x , c in enumerate(row):
            if not x in gx:
                nr.append('.')
            nr.append(c)    
        out.append(nr)
    return out

def toString(table):
    out = ""
    for row in table:
        for c in row:
            out += c
        out += '\n'
    return out

def dist(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def sumDist(image):
    galaxies = list(findGalaxies(image))
    dSum = 0
    for i,a in enumerate(galaxies):
        for b in galaxies[i:]:
            dSum += dist(a, b)
    return dSum


print("Part 1: ", sumDist(expand(image)))

def countLessThan(num, numbers):
    return len(list(filter(lambda x: x < num, numbers)))

age = 1000000 - 1

def expand2(image):
    galaxies = list(findGalaxies(image))
    gx = list(set(range(len(image[0]))) - set(map(lambda x: x[1], galaxies)))
    gy = list(set(range(len(image))) - set(map(lambda x: x[0], galaxies)))

    for galaxy in galaxies:
        x = age * countLessThan(galaxy[1], gx) + galaxy[1]
        y = age * countLessThan(galaxy[0], gy) + galaxy[0]
        yield (y,x)

def sumDistGalaxies(galaxies):
    dSum = 0
    for i,a in enumerate(galaxies):
        for b in galaxies[i:]:
            dSum += dist(a, b)
    return dSum


print("Part 2: ", sumDistGalaxies(list(expand2(image))))