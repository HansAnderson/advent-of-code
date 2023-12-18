#!/usr/bin/env python3
import itertools
import pathlib

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day18-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
#lines = example_1[1:-1].split("\n")

DIRS = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
}

def parse(is_part1=False):
    P = [(0, 0)]
    num_edges = 0
    for line in lines:
        d, n, cc = line.split()
        if is_part1:
            n = int(n)
        else:
            d = "RDLU"[int(cc[7], 16)]
            n = int(cc[2:7], 16)
        dx, dy = DIRS[d]
        P.append((P[-1][0] + (dx * n), P[-1][1] + (dy * n)))
        num_edges += n
    return P, num_edges

# Googling for interior of a polygon lead to "Shoelace formula".
def shoelace_trapezoid(points):
    return sum((y1 + y2) * (x1 - x2) for (x1, y1), (x2, y2) in itertools.pairwise(points)) / 2

p1P, p1E = parse(is_part1=True)
area = shoelace_trapezoid(p1P) + p1E / 2 + 1
print(str(area).rstrip(".0"))

p2P, p2E = parse()
area = shoelace_trapezoid(p2P) + p2E / 2 + 1
print(str(area).rstrip(".0"))
