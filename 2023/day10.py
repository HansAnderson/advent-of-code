#!/usr/bin/env python3
import itertools
import numpy as np
import pathlib
import pprint

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day10-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
.....
.S-7.
.|.|.
.L-J.
.....
"""
example_2 = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
example_3 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""
example_4 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""
example_5 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""
#lines = example_1[1:-1].split("\n")
#lines = example_2[1:-1].split("\n")
#lines = example_3[1:-1].split("\n")
#lines = example_4[1:-1].split("\n")
#lines = example_5[1:-1].split("\n")

DIRS = ((0,-1), (1, 0), (0, 1), (-1, 0))
NEXT = {
    "|": {(0, -1), (0, 1)},
    "-": {(1, 0), (-1, 0)},
    "L": {(0, -1), (1, 0)},
    "F": {(1, 0), (0, 1)},
    "J": {(0, -1), (-1, 0)},
    "7": {(0, 1), (-1, 0)},
}

DIM_X = len(lines[0])
DIM_Y = len(lines)
S = None

# find start
for y in range(DIM_Y):
    for x in range(DIM_X):
        if lines[y][x] == "S":
            S = (x, y)
            break
print(f"start: {S}")

# what are the next steps from S?
next_steps = []
for d in DIRS:
    p = np.array(S) + np.array(d)
    # is point valid in grid?
    if (p >= np.array([0, 0])).all() and (p < np.array([DIM_X, DIM_Y])).all():
        # is S reachable from point?
        if tuple(np.array(S) - p) in NEXT[lines[p[1]][p[0]]]:
            next_steps.append(tuple(p))
print(f"next steps: {next_steps}")

# pick a direction and run the loop
path = [S, next_steps[0]]
while True:
    cur_p = path[-1]
    last_dir = set((tuple(np.array(path[-2]) - np.array(path[-1])),))
    next_dir = NEXT[lines[cur_p[1]][cur_p[0]]] - last_dir
    assert len(next_dir) == 1
    next_p = tuple(np.array(cur_p) + np.array(next_dir.pop()))
    if next_p == S:
        # loop complete
        break
    path.append(next_p)

#pprint.pprint(path)
print(f"path len: {len(path)}")
print(f"part 1: {len(path)//2}")

def nwise(iterable, n=2):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    iters = itertools.tee(iterable, n)
    for i, it in enumerate(iters):
        for _ in range(i):
            next(it, None)
    return zip(*iters)

# sequence "right" and "left" turns
RP = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
R = list(nwise(RP))
LP = [(0, -1), (-1, 0), (0, 1), (1, 0), (0, -1)]
L = list(nwise(LP))

# count turns to figure out where interior is
r = 0
l = 0
for a, b, c in nwise(path + path[:2], n=3):
    turn = (tuple(np.array(b) - np.array(a)), tuple(np.array(c) - np.array(b)))
    if turn in R:
        r += 1
    if turn in L:
        l += 1
print(f"r={r}, l={l}")

# floodfill interior points with BFS
pipe = set(path)
I = set()
DP = RP if r > l else LP
for a, b in nwise(path, n=2):
    d = DP[DP.index(tuple(np.array(b) - np.array(a))) + 1]
    # for square a->b->c->d (where inputs are a,b), check c and d
    q = [tuple(np.array(b) + np.array(d)), tuple(np.array(a) + np.array(d))]
    while q:
        # ensure point does not cross bounds of pipe
        if (p := q.pop()) not in pipe:
            I.add(p)
            for d in DIRS:
                if (pp := tuple(np.array(p) + np.array(d))) not in I:
                    q.append(pp)

#print(I)
print(f"part 2: {len(I)}")
