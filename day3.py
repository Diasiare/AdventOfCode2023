import itertools
import operator
from functools import reduce

text = open("day3.txt").read()
lines = text.splitlines()


def getXY(matrix, y, x):
    if y < 0 or y >= len(matrix):
        return '.'
    line = matrix[y]
    if x < 0 or x >= len(line):
        return '.'
    return line[x]

def isSymbol(c):
    return not c.isnumeric() and not c == "."

ymods = [-1, 0, 1]
def symbolAround(matrix, y, x):
    for ym in ymods:
        if isSymbol(getXY(matrix, y + ym, x)):
            return True
    return False


    
count = 0

for ln, line in enumerate(lines):
    position = 0
    while position < len(line):
        if line[position].isnumeric():
            numbers = ""
            seenSymbol = symbolAround(lines, ln, position - 1)
            while position < len(line) and line[position].isnumeric():
                numbers = numbers + line[position]
                seenSymbol = seenSymbol or symbolAround(lines, ln, position)
                position += 1
            seenSymbol = seenSymbol or symbolAround(lines, ln, position)
            if seenSymbol:
                count += int(numbers)
        else:
            position += 1


print("Part 1: ", count)

def getFullNum(line, start):
    num = ""
    pos = start - 1
    while pos < len(line) and line[pos].isnumeric():
        num = line[pos] + num
        pos -= 1
    num = num + line[start]
    
    pos = start + 1
    while pos < len(line) and line[pos].isnumeric():
        num = num + line[pos]
        pos += 1
    return int(num), pos - start - 1

def numbersAround(matrix, y, x):
    numbers = []
    for ym in ymods:
        xm = -1
        while xm < 2:
            if getXY(matrix, y + ym, x + xm).isnumeric():
                number, extra = getFullNum(matrix[y + ym], x + xm)
                xm += extra
                numbers.append(number)
            xm += 1
    return numbers

count = 0

for ln, line in enumerate(lines):
    for lp, c in enumerate(line):
        if not c == "*":
            continue
        
        numbers = numbersAround(lines, ln, lp)
        if len(numbers) == 2:
            count += numbers[0] * numbers[1]


print("Part 2: ", count)