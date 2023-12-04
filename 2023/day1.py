#!/usr/bin/env python3
import pathlib
import re

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day1-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip('\n') for x in f]

example_1 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
example_2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
#lines = example_1[1:-1].split('\n')
#lines = example_2[1:-1].split('\n')

digit_words = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

def value(digit):
    try:
        return int(digit)
    except ValueError:
        return digit_words.index(digit) + 1

total = 0
for line in lines:
    digits = list(re.findall(r"(?=(-?\d|" + "|".join(digit_words) + "))", line))
    total += int(value(digits[0])) * 10 + value(digits[-1])

print(total)
