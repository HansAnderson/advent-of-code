#!/usr/bin/env python3
import pathlib

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day3-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip('\n') for x in f]

example_1 = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
#lines = example_1[1:-1].split('\n')

def nearby_symbols(x, y):
    syms = set()
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if 0 <= x + dx < len(lines[0]) and 0 <= y + dy < len(lines):
                ch = lines[y+dy][x+dx]
                if ch != "." and not ch.isdigit():
                    syms.add((x+dx, y+dy, ch))
    return syms

p1 = 0
p2 = 0

gear_nums = {}
num = ""
syms = set()

def finish_num(x, y):
    global p1, p2, gear_nums, num, syms
    #print(x, y, lines[y][x], num, syms)
    if syms:
        p1 += int(num)
    for sx, sy, sym in syms:
        if sym == "*":
            if (sx,sy) in gear_nums:
                p2 += int(num) * gear_nums[sx,sy]
            else:
                gear_nums[(sx,sy)] = int(num)
    num = ""
    syms = set()

for y, row in enumerate(lines):
    for x, ch in enumerate(row):
        if ch.isdigit():
            num += ch
            syms |= nearby_symbols(x, y)
        if num and (x+1 >= len(lines[0]) or not lines[y][x+1].isdigit()):
            finish_num(x, y)

print(p1)
print(p2)
