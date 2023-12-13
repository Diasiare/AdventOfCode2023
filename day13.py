import itertools
import operator
from functools import reduce

text = open("day13.txt").read()
patterns = list(map(lambda x : list(map(list,x.splitlines())),text.split('\n\n')))

def transpose(p):
    out = [[] for _ in range(len(p[0]))]
    for i, line in enumerate(p):
        for j, c in enumerate(line):
            out[j].append(c)

    return out


def reflectsAround(pattern, i):
    c = 0
    while i - c >=0 and i + 1 + c < len(pattern):
        if not pattern[i-c] == pattern[i + 1 + c]:
            return False
        c += 1
    return True

def findReflection(pattern):
    for i in range(len(pattern) - 1):
        if reflectsAround(pattern, i):
            return (i+1) * 100
    
    t = transpose(pattern)

    for i in range(len(t) - 1):
        if reflectsAround(t, i):
            return (i+1)
    
    return None



s = sum(map(findReflection, patterns))

print("Part 1: ", s)

def oposite(x):
    return "." if x == "#" else "#"

def findReflection2(pattern, ignore):
    for i in range(len(pattern) - 1):
        if reflectsAround(pattern, i):
            s = (i+1) * 100
            if ignore == s:
                continue
            return s
    
    t = transpose(pattern)

    for i in range(len(t) - 1):
        if reflectsAround(t, i):
            s = (i+1)
            if ignore == s:
                continue
            return s
    
    return None

def reflectSmudge(pattern):
    old = findReflection(pattern)
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            o = pattern[i][j]
            pattern[i][j] = oposite(o)
            r = findReflection2(pattern, old)
            if not r == None:
                return r
            pattern[i][j] = o
    

s = sum(map(reflectSmudge, patterns))

print("Part 2: ", s)