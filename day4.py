import itertools
import operator
from functools import reduce

text = open("day4.txt").read()
lines = text.splitlines()

def findUnion(line):
    mine, winning = line.split(': ')[1].split(' | ')
    mine = set([int(x) for x in mine.split()])
    winning = set([int(x) for x in winning.split()])
    win = len(mine.intersection(winning))
    return 0 if win == 0 else pow(2, win - 1)

score = sum([findUnion(line) for line in lines])

print("Part 1: ", score)

def findUnionCount(line):
    mine, winning = line.split(': ')[1].split(' | ')
    mine = set([int(x) for x in mine.split()])
    winning = set([int(x) for x in winning.split()])
    win = len(mine.intersection(winning))
    return win

counts = [1] * len(lines)
scores = [findUnionCount(line) for line in lines]

for i, v in enumerate(zip(counts, scores)):
    count, s = v
    for j in range(1, s+1):
        if i + j < len(counts):
            counts[i + j] += count

totalCards = sum(counts)

print("Part 2: ", totalCards)