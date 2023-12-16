import itertools
import operator
from functools import reduce

text = open("day5.txt").read()
sections = text.split("\n\n")

seeds = sections[0]
sections = sections[1:]

seeds = [int(x) for x in seeds.removeprefix("seeds: ").split()]

def parseSection(section):
    lines = section.splitlines()
    f, to = lines[0].removesuffix(' map:').split('-to-')
    ranges = [tuple([int(x) for x in line.split()]) for line in lines[1:]]
    ranges.sort(key=lambda x: x[1])
    return (f, (to, ranges))

rMaps = {
}
for section in sections:
    f, cont = parseSection(section)
    rMaps[f] = cont

def numberToNext(number, ranges):
    for dest, source, length in ranges:
        sub = number - source
        if sub >= 0 and sub < length:
            return dest + sub
    return number

source = "seed"
sourceValues = seeds

while not source == "location":
    destValues = []
    dest, ranges = rMaps[source]
    for val in sourceValues:
        destValues.append(numberToNext(val, ranges))
    source = dest
    sourceValues = destValues

print("Part 1: ", min(sourceValues))

#ranges are (start, length)

startRanges = []
for i in range(0, len(seeds), 2):
    startRanges.append((seeds[i], seeds[i+1]))

def extend(l, value):
    copy = list(l)
    copy.extend(value)
    return copy

def rangeToNext(r, ranges):
    rstart, rlength = r
    if rlength <= 0:
        return  []
    rendEx = rstart + rlength
    for dest, source, length in ranges:
        endEx = source + length
        if rstart >= source and rendEx <= endEx:
            return [(dest + rstart - source, rlength)]
        if rstart >= source and rstart < endEx:
            return extend([(dest + rstart - source, rlength - (rendEx - endEx))], rangeToNext((endEx, rendEx - endEx), ranges))
        if rstart < source and rendEx > source and rendEx < endEx:
            return extend(rangeToNext((rstart, source - rstart), ranges), [(dest, rlength - (source  - rstart))])
        if rstart <= source and rendEx > endEx:
            before = rangeToNext((rstart, source - rstart),ranges)
            middle = [(dest, length)]
            end = rangeToNext((endEx, rendEx - endEx), ranges)
            return extend(before, extend(middle, end))
    return [r]

source = "seed"
sourceRanges = startRanges

while not source == "location":
    destRanges = []
    dest, ranges = rMaps[source]
    for val in sourceRanges:
        values = rangeToNext(val, ranges)
        destRanges.extend(values)
    source = dest
    sourceRanges = destRanges

starts = [x[0] for x in sourceRanges]

print("Part 2: ", min(starts))