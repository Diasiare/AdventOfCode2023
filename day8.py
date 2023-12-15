import itertools
import operator
from functools import reduce
from math import lcm

text = open("day8.txt").read()
lines = text.splitlines()

instructions = lines[0]
networkText = lines[2:]
network = {}

for line in networkText:
    name, n = line.split(' = ')
    n = n.removesuffix(')').removeprefix('(')
    left, right = n.split(', ')
    network[name] = (left, right)

def next(network, current,step):
    left, right = network[current]
    return left if s == 'L' else right

current = "AAA"
steps = 0
while not current == "ZZZ":
    s = instructions[steps % len(instructions)]
    current = next(network, current, s)
    steps += 1


print("Part 1: ", steps)

positions = [x for x in network if x.endswith("A")]
steps = 0

memory = [[] for _ in positions]

while not all(map(lambda x: len(x) > 1, memory)):
    s = instructions[steps % len(instructions)]
    steps += 1
    for i in range(len(positions)):
        positions[i] = next(network, positions[i], s)
        if (positions[i].endswith('Z')):
            memory[i].append((steps, 0 if len(memory[i]) == 0 else steps - memory[i][-1][0]))

cyleLength = [x[0][0]  for x in memory]

print("Part 2: ", lcm(*cyleLength))