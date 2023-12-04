#!/usr/bin/env python3
import math
import pathlib

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day2-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip('\n') for x in f]

example_1 = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
#lines = example_1[1:-1].split('\n')

max_cubes = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

p1 = 0
p2 = 0
for line in lines:
    game_id = int(line.split(":")[0].split(" ")[1])
    sets = line.split(":")[1].split(";")
    #print(game_id, sets)
    possible = True
    min_cubes = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }
    for s in sets:
        for count, color in [x.strip().split(" ") for x in s.split(",")]:
            count = int(count)
            if count > max_cubes[color]:
                possible = False
            if count > min_cubes[color]:
                min_cubes[color] = count
    if possible:
        p1 += game_id
    p2 += math.prod(min_cubes.values())

print(p1)
print(p2)
