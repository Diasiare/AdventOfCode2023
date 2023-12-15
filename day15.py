import itertools
from collections import OrderedDict
import collections
from functools import reduce

text = open("day15.txt").read()
lines = text.splitlines()

inp = text.replace("\n", "")

def hash(s):
    val = 0
    for c in s:
        value = ord(c)
        val += value
        val *= 17
        val = val % 256
    return val

count = 0
for s in inp.split(","):
    count += hash(s)


print("Part 1: ", count)

boxes = [''] * 256
boxes = [OrderedDict() for _ in boxes]

for part in inp.split(","):
    if part.endswith('-'):
        label = part.replace('-', '')
        box = hash(label)
        if label in boxes[box]:
            del boxes[box][label]
    else:
        label, lens = part.split('=')
        box = hash(label)
        boxes[box][label] = int(lens)

power = 0
for i, box in enumerate(boxes):
    for j, key in enumerate(box):
        power += (i+1) * (j+1) * box[key]


print("Part 2: ", power)