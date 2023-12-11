#!/usr/bin/env python3
import itertools
import numpy as np
import pathlib
import pprint

NPA = np.array

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day11-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
#lines = example_1[1:-1].split("\n")

U = [[x for x in y] for y in lines]
#pprint.pprint(U)

G = [(x, y) for x in range(len(U[0])) for y in range(len(U)) if U[y][x] == "#"]
#pprint.pprint(G)

def expand(n):
    global G
    global U

    NG = G.copy()

    for y in reversed(range(len(U))):
        if all(x == "." for x in U[y]):
            for i, g in enumerate(NG):
                if g[1] > y:
                    NG[i] = tuple(NPA(g) + NPA([0, n]))

    for x in reversed(range(len(U[0]))):
        if all(y[x] == "." for y in U):
            for i, g in enumerate(NG):
                if g[0] > x:
                    NG[i] = tuple(NPA(g) + NPA([n, 0]))

    return NG

Gp1 = expand(1)
#pprint.pprint(Gp1)
p1 = 0
for g1, g2 in itertools.combinations(Gp1, r=2):
    d = NPA(g2) - NPA(g1)
    p1 += np.abs(d).sum()
print(f"part 1: {p1}")

#Gp2 = expand(10 - 1)
#Gp2 = expand(100 - 1)
Gp2 = expand(1000000 - 1)
p2 = 0
for g1, g2 in itertools.combinations(Gp2, r=2):
    d = NPA(g2) - NPA(g1)
    p2 += np.abs(d).sum()
print(f"part 2: {p2}")
