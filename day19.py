import itertools
import operator
from functools import reduce

text = open("day19.txt").read()
workflows, ratings = [x.splitlines() for x in text.split("\n\n")]

def parseRating(ratingLine):
    ratingLine = ratingLine.removeprefix("{").removesuffix("}")
    out = {}
    for part in ratingLine.split(','):
        k,v = part.split('=')
        out[k] = int(v)
    return out

def parseWorkflow(workflowLine):
    name, flow = workflowLine.removesuffix('}').split('{')
    parts = flow.split(',')
    default = parts[-1]
    parts = parts[:-1]
    evals = []
    for part in parts:
        comparison, target = part.split(':')
        key = comparison[0]
        op = comparison[1]
        value = int(comparison[2:])
        evals.append((key, op , value, target))
    return (name, evals, default)

ratings = [parseRating(x) for x in ratings]
workflows = [parseWorkflow(x) for x in workflows]
workflowMap = {}
for name, parts, default in workflows:
    workflowMap[name] = (parts, default)

def runOn(workflow, ratings):
    parts,default = workflow

    for key, op, value, target in parts:
        ratingValue = ratings[key]
        f = None
        if op == '<':
            f = ratingValue < value
        else:
            f = ratingValue > value
        if f:
            return target
        
    return default

def evaluateFully(workflowMap, ratings):
    wfName = 'in'

    while True:
        wfName = runOn(workflowMap[wfName], ratings)
        if wfName in ['A', 'R']:
            return wfName

score = 0
for rating in ratings:
    r = evaluateFully(workflowMap, rating)
    if r == 'A':
        score += sum(rating.values())

print("Part 1: ", score)

baseMap = {
    'x': (1, 4000),
    'm': (1, 4000),
    'a': (1, 4000),
    's': (1, 4000),
}

front = [('in', baseMap)]

def split(ratingRange, value):
    if (ratingRange[1] < value):
        return (ratingRange, None)
    if (ratingRange[0] > value):
        return (None, ratingRange)
    return ((ratingRange[0], value - 1), (value + 1, ratingRange[1]))

# returns (hit, miss)
def splitBy(workflowPart, ratingMap):
    key, op, value, _ = workflowPart
    ratingRange = ratingMap[key]
    first, second = split(ratingRange, value)
    hitMap = ratingMap.copy()
    missMap = ratingMap.copy()
    if op == '<':
        second = None if second == None else (second[0] - 1, second[1])
        hitMap[key] = first
        missMap[key] = second
    else:
        first = None if first == None else (first[0], first[1] + 1)
        hitMap[key] = second
        missMap[key] = first
    return (hitMap, missMap)

def isValid(ratingMap):
    return all([(not v == None) and v[0] <= v[1] for v in ratingMap.values()])

def divideUp(workflow, ratingMap):
    parts, default = workflow
    out = []
    for part in parts:
        target = part[-1]
        hit, miss = splitBy(part, ratingMap)
        if isValid(hit):
            out.append((target, hit))
        if not isValid(miss):
            return out
        ratingMap = miss
    out.append((default, ratingMap))
    return out

def calcScore(ratingMap):
    return reduce(lambda a,b: a*b, [a[1] - a[0] + 1 for a in ratingMap.values()], 1)

score = 0

while len(front) > 0:
    workflowName, ratingMap = front.pop()
    newWorkflows = divideUp(workflowMap[workflowName], ratingMap)

    for newWorkflow in newWorkflows:
        workflowName, ratingMap = newWorkflow
        if workflowName == 'R':
            continue
        elif workflowName ==  'A':
            score += calcScore(ratingMap) 
        else:
            front.append(newWorkflow)


print("Part 2: ", score)