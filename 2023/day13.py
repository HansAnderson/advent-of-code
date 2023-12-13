#!/usr/bin/env python3
import pathlib

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day13-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
#lines = example_1[1:-1].split("\n")

# re-group lines in double-newline splits
groups = [x.split("\n") for x in ("\n".join(lines)).split("\n\n")]

def check_x(lines):
    xdiffs = []
    for x in range(1, len(lines[0])):
        diff = sum(lines[y][x + dx] != lines[y][x - dx - 1] for y in range(len(lines)) for dx in range(min(x, len(lines[0]) - x)))
        #print(f"  x={x}, diff={diff}")
        xdiffs.append((diff, x))
    return sorted(xdiffs)

def check_y(lines):
    ydiffs = []
    for y in range(1, len(lines)):
        diff = sum(lines[y + dy][x] != lines[y - dy - 1][x] for x in range(len(lines[0])) for dy in range(min(y, len(lines) - y)))
        #print(f"  y={y}, diff={diff}")
        ydiffs.append((diff, y))
    return sorted(ydiffs)

p1 = 0
p2 = 0
for i, group in enumerate(groups):
    xdiffs = check_x(group)
    ydiffs = check_y(group)
    for diff, x in xdiffs:
        if diff == 0:
            print(f"{i} fold x={x}")
            p1 += x
        elif diff == 1:
            print(f"{i} smudge x={x}")
            p2 += x
    for diff, y in ydiffs:
        if diff == 0:
            print(f"{i} fold y={y}")
            p1 += 100 * y
        elif diff == 1:
            print(f"{i} smudge y={y}")
            p2 += 100 * y
print(p1)
print(p2)
