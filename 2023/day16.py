#!/usr/bin/env python3
import pathlib

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day16-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
#lines = example_1[1:-1].split("\n")

X = len(lines[0])
Y = len(lines)

def next_beam(x, y, dx, dy):
    return ((x + dx, y + dy), (dx, dy))

def run(S):
    beams = [S]
    states = set()
    visited = set()

    while beams:
        beam = beams.pop()
        (x, y), (dx, dy) = beam
        if x < 0 or x >= X or y < 0 or y >= Y:
            continue
        if beam in states:
            continue
        states.add(beam)
        visited.add((x, y))
        t = lines[y][x]
        if t == "." or (t == "-" and dx != 0) or (t == "|" and dy != 0):
            beams.append(next_beam(x, y, dx, dy))
        elif t == "|":
            beams.extend(next_beam(x, y, *v) for v in ((0, -1), (0, 1)))
        elif t == "-":
            beams.extend(next_beam(x, y, *v) for v in ((-1, 0), (1, 0)))
        elif t == "/":
            beams.append(next_beam(x, y, -dy, -dx))
        elif t == "\\":
            beams.append(next_beam(x, y, dy, dx))
    return len(visited)

p1 = run(((0, 0), (1, 0)))
print(p1)

p2 = 0
for y in range(Y):
    for x in range(X):
        if x == 0:
            dx, dy = (1, 0)
        elif x == X-1:
            dx, dy = (-1, 0)
        elif y == 0:
            dx, dy = (0, 1)
        elif y == Y-1:
            dx, dy = (0, -1)
        else:
            continue
        p2 = max(p2, run(((x, y), (dx, dy))))
print(p2)
