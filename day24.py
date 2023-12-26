import itertools
import operator
from functools import reduce
from sympy import Symbol
from sympy import solve_poly_system

text = open("day24.txt").read()
lines = text.splitlines()

def toPath(line):
    pos, vel = line.split(" @ ")
    pos = tuple([int(x) for x in pos.split(", ")])
    vel = tuple([int(x) for x in vel.split(", ")])
    return (pos, vel)


def toLineEquation(line):
    pos, vel = line
    px, py, _ = pos
    dx, dy, _ = vel

    c = py - (dy * px / dx)
    a = dy / dx
    return (a, c)

paths = [toPath(x) for x in lines]

def lineIntersection(lineEq1, lineEq2):
    a, c = lineEq1
    b, d = lineEq2

    if a == b:
        return None

    return ((d - c) / (a - b), a* ((d - c) / (a - b)) + c)

def pointInFuture(point, path):
    x, _ = point
    cx = path[0][0]
    dx = path[1][0]

    if x == cx:
        return True
    if x > cx:
        return dx > 0
    return dx < 0 

volume = (200000000000000, 400000000000000)

count = 0
for i, path in enumerate(paths[:-1]):
    for path2 in paths[i + 1:]:
        point = lineIntersection(toLineEquation(path), toLineEquation(path2))
        if point == None:
            continue
        if not pointInFuture(point, path) or not pointInFuture(point, path2):
            continue
        
        if all([v >= volume[0] and v <= volume[1] for v in point]):
            count += 1



# x = px + dx*t
# y = py + dy*t
# t = (x - px)/dx
# y = py - dy * px / dx + x * dy / dx

print("Part 1: ", count)

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
vx = Symbol('vx')
vy = Symbol('vy')
vz = Symbol('vz')


equations = []
t_syms = []
for i, path in enumerate(paths[:3]):
    s, vel = path
    lpx, lpy, lpz = s
    ldx, ldy, ldz = vel
    t = Symbol('t'+str(i))
    t_syms.append(t)
    equations.append( x + vx*t - lpx - ldx*t)
    equations.append( y + vy*t - lpy - ldy*t)
    equations.append( z + vz*t - lpz - ldz*t)


# find a px, py, pz , dx, dy, dz such that
# for all lines (lpx, lpy, lpz, ldx, ldy, ldz) there exists a t such that 
# px + dx * t = lpx + ldx * t
# (px - lpx) / (ldx - dx) = t
# (px - lpx) / (ldx - dx) = (py - lpy) / (ldy - dy) = (pz - lpz) / (ldz - dz)


result = solve_poly_system(equations,*([x,y,z,vx,vy,vz]+t_syms))
print("Part 2: ", result[0][0]+result[0][1]+result[0][2])