import itertools
import operator
from functools import reduce

text = open("day2.txt").read()
lines = text.splitlines()

def parseLine(line):
    rounds = line.split(":")[1].strip().split(";")
    out = []
    for round in rounds:
        colors = round.split(",")
        d = {}
        for color in colors:
            count, draw = color.strip().split(" ")
            d[draw] = int(count)
        out.append(d)
    return out

games = list(map(parseLine, lines))

def colorCount(map, color):
    if color in map:
        return map[color]
    return 0

count = 0
for i, game in enumerate(games):
    success = True
    for round in game:
        success = success and colorCount(round, "blue") < 15 and colorCount(round, "red") < 13 and colorCount(round, "green") < 14
    if success:
        count = count + i + 1

print("Part 1: ", count)

count = 0
for game in games:
    b = max(map(lambda r: colorCount(r, "blue"), game))
    g = max(map(lambda r: colorCount(r, "green"), game))
    r = max(map(lambda r: colorCount(r, "red"), game))
    count += r * g * b

print("Part 2: ", count)