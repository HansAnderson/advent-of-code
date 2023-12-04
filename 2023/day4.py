#!/usr/bin/env python3
import pathlib
import re

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day4-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip('\n') for x in f]

example_1 = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
#lines = example_1[1:-1].split('\n')

p1 = 0
cards = [1] * len(lines)

for i, line in enumerate(lines):
    lnums, rnums = [set(int(x) for x in re.findall(r"-?\d+", y)) for y in line.split(":")[1].split("|")]
    if (nums := lnums & rnums):
        p1 += 2**(len(nums)-1)
        for j in range(1,len(nums)+1):
            if i+j < len(lines):
                cards[i+j] += cards[i]

print(p1)
print(sum(cards))
