#!/usr/bin/env python3
import math
import pathlib

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day6-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
Time:      7  15   30
Distance:  9  40  200
"""
#lines = example_1[1:-1].split("\n")

times = [int(x) for x in lines[0].split(":")[1].split()]
distances = [int(x) for x in lines[1].split(":")[1].split()]


def slow(t, d):
    wins = 0
    for i in range(t):
        if (t - i) * i > d:
            wins += 1
    return wins

def fast(t, d):
    # https://www.wolframalpha.com/input?i=solve+%28t+-+x%29+*+x+%3E+d+for+x
    # 1/2 (t - sqrt(t^2 - 4 d))<x<1/2 (sqrt(t^2 - 4 d) + t) and d<t^2/4 and t element R
    min_ = .5 * (t - math.sqrt(t**2 - 4 * d))
    max_ = .5 * (math.sqrt(t**2 - 4 * d) + t)
    return math.ceil(max_ - 1) - math.floor(min_ + 1) + 1

#method = slow
method = fast

p1 = 1
for t, d in zip(times, distances):
    p1 *= method(t, d)
print(p1)

t = int("".join(lines[0].split(":")[1].split()))
d = int("".join(lines[1].split(":")[1].split()))
p2 = method(t, d)
print(p2)
