import itertools
import operator
from functools import reduce

text = open("day7.txt").read()
lines = text.splitlines()

def handType(hand):
    counts = {}
    for c in hand:
        if c in counts:
            counts[c] += 1
        else:
            counts[c] = 1
    values = [counts[k] for k in counts]
    values.sort()

    if len(values) == 1:
        return 7
    if values[-1] == 4:
        return 6
    if values[-1] == 3 and values[0] == 2:
        return 5
    if values[-1] == 3:
        return 4
    if len(list([x for x in values if x == 2])) == 2:
        return 3
    if values[-1] == 2:
        return 2
    return 1

def ordinal(c):
    if c == 'A':
        return 14
    if c == 'K':
        return 13
    if c == 'Q':
        return 12
    if c == 'J':
        return 11
    if c == 'T':
        return 10
    return int(c)

def ordinals(hand):
    out = []
    for c in hand:
        out.append(ordinal(c))
    return tuple(out) 

def toSortable(line):
    hand, bet = line.split(' ')
    ht = handType(hand)
    o = ordinals(hand)
    bet = int(bet)
    return (ht, o , bet)

games = [toSortable(x) for x in lines]
games.sort()

score = 0
for i, v in enumerate(games):
    score += (i+1) * v[2]

print("Part 1: ", score)

def handType2(hand):
    counts = {}
    for c in hand:
        if c in counts:
            counts[c] += 1
        else:
            counts[c] = 1
    jcount = 0
    if 'J' in counts:
        jcount = counts['J']
        del counts['J']
    values = [counts[k] for k in counts]
    values.sort()
    if len(values) == 0:
        values = [0]


    if len(values) == 1:
        return 7
    if values[-1] + jcount == 4:
        return 6
    if len(values) == 2:
        return 5
    if values[-1] + jcount == 3:
        return 4
    if values[-1] + jcount >= 2 and values[-2] + max(0, jcount - (2 - values[-1])) >= 2:
        return 3
    if values[-1] + jcount == 2:
        return 2
    return 1

def ordinal2(c):
    if c == 'A':
        return 14
    if c == 'K':
        return 13
    if c == 'Q':
        return 12
    if c == 'J':
        return 1
    if c == 'T':
        return 10
    return int(c)

def ordinals2(hand):
    out = []
    for c in hand:
        out.append(ordinal2(c))
    return tuple(out) 

def toSortable2(line):
    hand, bet = line.split(' ')
    ht = handType2(hand)
    o = ordinals2(hand)
    bet = int(bet)
    return (ht, o , bet)

games = [toSortable2(x) for x in lines]
games.sort()

score = 0
for i, v in enumerate(games):
    score += (i+1) * v[2]


print("Part 2: ", score)