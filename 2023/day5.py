#!/usr/bin/env python3
import pathlib
import re

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day5-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
#lines = example_1[1:-1].split("\n")

# re-group lines in double-newline splits
groups = [x.split("\n") for x in ("\n".join(lines)).split("\n\n")]

mappings = [[[int(x) for x in y.split()] for y in group[1:]] for group in groups[1:]]
#print(mappings)

# part 1
seeds = [int(x) for x in re.findall(r"\d+", groups[0][0])]
for mapping in mappings:
    for i, seed in enumerate(seeds):
        for dst, src, len_ in mapping:
            if src <= seed < src + len_:
                seeds[i] = dst + (seed - src)
                break
print(min(seeds))

# part 2
seed_ranges = [[int(x) for x in y.split()] for y in re.findall(r"\d+ \d+", groups[0][0])]
for mapping in mappings:
    translated = []
    for dst, src, len_ in mapping:
        untranslated = []
        for sstart, slen in seed_ranges:
            if sstart + slen <= src or sstart >= src + len_:
                # no overlap
                untranslated.append([sstart, slen])
                continue
            if sstart < src:
                # start before, chop off start
                untranslated.append([sstart, src - sstart])
            if sstart + slen > src + len_:
                # ends after, chop off end
                untranslated.append([src + len_, (sstart + slen) - (src + len_)])
            if sstart < src + len_ and sstart + slen > src:
                # translate within range
                start = max(sstart, src)
                end = min(sstart + slen, src + len_)
                translated.append([start + (dst - src), end - start])
        #print(translated, untranslated)
        seed_ranges = untranslated
    seed_ranges = sorted(translated + untranslated)
    #print()

# ranges are sorted by location start, so the first start is the lowest value
print(seed_ranges[0][0])
