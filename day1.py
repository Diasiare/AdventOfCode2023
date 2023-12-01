import itertools
import operator
from functools import reduce

text = open("day1.txt").read()
lines = text.splitlines()


sum = 0
for line in lines:
    first = 0
    last = 0
    counter = 0
    while counter < len(line):
        counter += 1
        if line[counter - 1].isdigit():
            first = int(line[counter-1])
            last = int(line[counter-1])
            break

    while counter < len(line):
        counter += 1
        if line[counter - 1].isdigit():
            last = int(line[counter-1])
    sum += first * 10 + last

print("Part 1: ", sum)

sequences = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "zero": 0,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

sequences = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "zero": 0,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def match(line, pos):
    for key, value in sequences.items():
        if line[pos:].startswith(key):
            return value
    return None

sum = 0
for line in lines:
    first = 0
    last = 0
    counter = 0
    while counter < len(line):
        counter += 1
        val = match(line, counter - 1)
        if val != None:
            first = val
            last = val
            break

    while counter < len(line):
        counter += 1
        val = match(line, counter - 1)
        if val != None:
            last = val
    sum += first * 10 + last


print("Part 2: ", sum)