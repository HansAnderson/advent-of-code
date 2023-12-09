#!/usr/bin/env python3
import itertools
import pathlib
import re

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day9-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
#lines = example_1[1:-1].split("\n")

def pairwise(iterable):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def reduce_(row, is_part2=False):
    if all(x == 0 for x in row):
        return (0, 0)
    l, r = reduce_([b - a for (a, b) in pairwise(row)])
    return (row[0] - l, row[-1] + r)

p1 = 0
p2 = 0
for line in lines:
    nums = [int(x) for x in re.findall(r"-?\d+", line)]
    l, r = reduce_(nums)
    p1 += r
    p2 += l
print(p1)
print(p2)
