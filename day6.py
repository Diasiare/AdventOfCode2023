import itertools
import operator
from functools import reduce

text = open("day6.txt").read()
times, distances = text.splitlines()

def parse(s):
    return [int(x) for x in s.split()]

times = parse(times.removeprefix("Time:"))
distances = parse(distances.removeprefix("Distance:"))

def timeCount(time, distance):
    count = 0
    for tHeld in range(time):
        dTravel = (time - tHeld)*tHeld
        if dTravel > distance:
            count += 1
    return count

count = reduce(lambda a, b: a*b, [timeCount(*x) for x in zip(times, distances)] , 1)

print("Part 1: ", count)

time = int(''.join([str(x) for x in times]))
distance = int(''.join([str(x) for x in distances]))

count = timeCount(time, distance)

print("Part 2: ", count)