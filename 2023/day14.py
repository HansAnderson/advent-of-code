#!/usr/bin/env python3
import pathlib

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day14-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
#lines = example_1[1:-1].split("\n")

## original part 1
#p1 = 0
#for x in range(len(lines[0])):
#    sup = len(lines)
#    for y in range(len(lines)):
#        ch = lines[y][x]
#        if ch == "#":
#            sup = len(lines) - y - 1
#        elif ch == "O":
#            p1 += sup
#            sup -= 1
#print(p1)

O = set((x, y) for x in range(len(lines[0])) for y in range(len(lines)) if lines[y][x] == "O")
H = set((x, y) for x in range(len(lines[0])) for y in range(len(lines)) if lines[y][x] == "#")

def north(o):
    global H
    for x in range(len(lines[0])):
        sup = 0
        for y in range(len(lines)):
            p = (x, y)
            if p in H:
                sup = y + 1
            elif p in o:
                o.remove(p)
                o.add((x, sup))
                sup += 1

def west(o):
    global H
    for y in range(len(lines)):
        sup = 0
        for x in range(len(lines[0])):
            p = (x, y)
            if p in H:
                sup = x + 1
            elif p in o:
                o.remove(p)
                o.add((sup, y))
                sup += 1

def south(o):
    global H
    for x in range(len(lines[0])):
        sup = len(lines) - 1
        for y in reversed(range(len(lines))):
            p = (x, y)
            if p in H:
                sup = y - 1
            elif p in o:
                o.remove(p)
                o.add((x, sup))
                sup -= 1

def east(o):
    global H
    for y in range(len(lines)):
        sup = len(lines[0]) - 1
        for x in reversed(range(len(lines[0]))):
            p = (x, y)
            if p in H:
                sup = x - 1
            elif p in o:
                o.remove(p)
                o.add((sup, y))
                sup -= 1

def calc_north_load(o):
    load = 0
    for p in o:
        load += len(lines) - p[1]
    return load

def tilt(o, n):
    o = o.copy()
    cache = {}
    for i in range(n):
        io = frozenset(o)
        if (ci := cache.get(io)) is not None:
            period = i - ci
            # extra +1 because the output is the next cached item
            need = (n - 1 - ci + 1) % period + ci
            print(f"{i} is {ci} period {period}, need {need}")
            for o, j in cache.items():
                if j == need:
                    return o
        else:
            north(o)
            west(o)
            south(o)
            east(o)
            cache[io] = i
            #print(i, calc_north_load(o))
    return o

Op1 = O.copy()
north(Op1)
print(calc_north_load(Op1))

Op2 = tilt(O, 1000000000)
print(calc_north_load(Op2))
