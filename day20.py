import itertools
import operator
from functools import reduce
import queue
from math import lcm

text = open("day20.txt").read()
lines = text.splitlines()

def parse(module):
    name, targets = module.split(' -> ')
    targets = targets.split(', ')
    if not name[0] in ['%', '&']:
        return (name, name, targets)
    
    t = name[0]
    name = name[1:]
    return (name, t, targets)

modules = [parse(x) for x in lines]
moduleMap = {}
for name, t, targets in modules:
    moduleMap[name] = (t, targets)

flipModuleStates = {}
conjunctionStates = {}
for name, t, targets in modules:
    if t == '%':
        flipModuleStates[name] = False
    elif t == '&':
        conjunctionStates[name] = {}
for name, t, targets in modules:
    for target in targets:
        if not target in conjunctionStates:
            continue
        conjunctionStates[target][name] = False

#  (source, isHigh, target)
processQueue = queue.Queue()

counters = {
    True: 0,
    False: 0,
}

for i in range(1000):
#for i in range(1):
    
    processQueue.put(('button', False, 'broadcaster'))
    while not processQueue.empty():
        source, isHigh, oTarget = processQueue.get()
        counters[isHigh] += 1

        if not oTarget in moduleMap:
            continue
        t, targets = moduleMap[oTarget]

        value = None
        if t == 'broadcaster':
            value = isHigh
        elif t == '%':
            if not isHigh:
                value = not flipModuleStates[oTarget]
                flipModuleStates[oTarget] = value
        elif t == '&':
            conjunctionStates[oTarget][source] = isHigh
            value = not all(conjunctionStates[oTarget].values())

        if value == None:
            continue 
        for target in targets:
            processQueue.put((oTarget, value, target))


print("Part 1: ", counters[True] * counters[False])

flipModuleStates = {}
conjunctionStates = {}
for name, t, targets in modules:
    if t == '%':
        flipModuleStates[name] = False
    elif t == '&':
        conjunctionStates[name] = {}
for name, t, targets in modules:
    for target in targets:
        if not target in conjunctionStates:
            continue
        conjunctionStates[target][name] = False

conds = None
condsTarget = None
for source, t, target in modules:
    if not 'rx' in target:
        continue
    conds = {}
    condsTarget = source
    for key in conjunctionStates[source]:
        conds[key] = []
    break


found = False
counter = 0
while not all([len(x) > 1 for x in conds.values()]):
    processQueue.put(('button', False, 'broadcaster'))
    counter += 1
    seen = set()
    while not processQueue.empty():
        source, isHigh, oTarget = processQueue.get()

        if oTarget == condsTarget and isHigh:
            conds[source].append(counter)

        if not oTarget in moduleMap:
            continue
        t, targets = moduleMap[oTarget]

        value = None
        if t == 'broadcaster':
            value = isHigh
        elif t == '%':
            if not isHigh:
                value = not flipModuleStates[oTarget]
                flipModuleStates[oTarget] = value
        elif t == '&':
            conjunctionStates[oTarget][source] = isHigh
            value = not all(conjunctionStates[oTarget].values())

        if value == None:
            continue 
        for target in targets:
            processQueue.put((oTarget, value, target))

for key in conds:
    values = conds[key]
    base = values[0]
    second = values[1]
    conds[key] = second - base

print("Part 2: ", lcm(*list(conds.values())))