import itertools
import operator
from functools import reduce

text = open("day12.txt").read()
lines = text.splitlines()

def parse(l):
    s, nums = l.split(' ')
    return (list(s), list(map(int, nums.split(','))))

inp = list(map(parse, lines))

def isValid(list, numbers):
    c = 0
    numIn = 0
    while c < len(list):
        if list[c] == '#':
            if numIn >= len(numbers):
                return False
            l = list[c: c+numbers[numIn]]
            if '.' in l:
                return False
            if len(l) < numbers[numIn]:
                return False
            if  c + numbers[numIn] < len(list) and list[c + numbers[numIn]]  == '#':
                return False
            c += numbers[numIn]
            numIn += 1
            continue
        c += 1
    return numIn == len(numbers)

def search1(list, numbers, index):
    if index == len(list):
        if isValid(list, numbers):
            return 1
        return 0
    
    c = list[index]
    if not c == "?":
        return search1(list, numbers, index + 1)
    
    list[index] = "."
    count = search1(list, numbers, index + 1)
    list[index] = "#"
    count += search1(list, numbers, index + 1)
    list[index] = "?"
    return count


def searchSub(list, numbers, cache):
    if len(list) == 0:
        #print(0, 2)
        return 0

    if list[0] == '#':
        c = list[0:numbers[0]]
        if '.' in c or len(c) < numbers[0]:
            #print(0, 3)
            return 0
        list = list[numbers[0]:]
        if len(list) > 0 and list[0] == '#':
            #print(0, 4)
            return 0
        return search(list[1:], numbers[1:], cache)
    
    c = list[0:numbers[0]]
    if '.' in c or len(c) < numbers[0]:
        return search(list[1:], numbers, cache)
    
    if len(list) > numbers[0] and list[numbers[0]] == '#':
        return search(list[1:], numbers, cache)
    
    return search(list[numbers[0]+1:], numbers[1:], cache) + search(list[1:], numbers, cache)

def search(list, numbers, cache):
    #print(list, numbers)
    if numbers == []:
        if '#' in list:
            #print(0, 0)
            return 0
        #print(1 , 1)
        return 1 
    
    c = 0
    while c < len(list) and list[c] == '.':
        c += 1
    list = list[c:]
    if (len(list),len(numbers)) in cache:
        return cache[(len(list),len(numbers))]
    rv = searchSub(list, numbers, cache)
    cache[(len(list),len(numbers))] = rv
    return rv
  
    
    
s = 0
for l, numbers in inp:
    count2 = search(l, numbers, {})
    s += count2

print("Part 1: ", s)

t5 = list(map(lambda x : (x[0] + ["?"] + x[0] + ["?"] +x[0] + ["?"] +x[0] + ["?"] +x[0], x[1] * 5), inp))

s = 0
for l, numbers in t5:
    count = search(l,numbers, {})
    #print(l, numbers, count)
    s += count


print("Part 2: ", s)