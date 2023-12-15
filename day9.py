import itertools
import operator
from functools import reduce

text = open("day9.txt").read()
lines = text.splitlines()
inp = [list(map(int, x.split(' '))) for x in lines]

def computeLast(numberList):
    subNumbers = []
    allZero = True
    for a,b in zip(numberList[:len(numberList) - 1], numberList[1:]):
        num  = b - a
        if not num == 0:
            allZero = False
        subNumbers.append(num)
    if allZero:
        return numberList[-1]
    else:
        return numberList[-1] + computeLast(subNumbers)
    
count = 0
for seq in inp:
    val = computeLast(seq)
    count += val

print("Part 1: ", count)

def computeFirst(numberList):
    subNumbers = []
    allZero = True
    for a,b in zip(numberList[:len(numberList) - 1], numberList[1:]):
        num  = b - a
        if not num == 0:
            allZero = False
        subNumbers.append(num)
    if allZero:
        return numberList[0]
    else:
        return numberList[0] - computeFirst(subNumbers)
    
count = 0
for seq in inp:
    val = computeFirst(seq)
    count += val


print("Part 2: ", count)