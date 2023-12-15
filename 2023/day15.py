#!/usr/bin/env python3
import collections
import pathlib

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day15-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
#lines = example_1[1:-1].split("\n")

def hash_(s):
    h = 0
    for c in s:
        h = ((h + ord(c)) * 17) % 256
    return h

assert hash_("HASH") == 52

print(sum(hash_(x) for x in lines[0].split(",")))

# python dicts have all the required properties for lense order
boxes = collections.defaultdict(dict)
for step in lines[0].split(","):
    if step[-1] == "-":
        lbl = step[:-1]
        boxes[hash_(lbl)].pop(lbl, None)
    else:
        lbl, fl = step.split("=")
        boxes[hash_(lbl)][lbl] = fl
    if 0:
        print(step)
        for h, box in boxes.items():
            if box:
                print(h, list(box.items()))

p2 = 0
for h, box in boxes.items():
    for slot, (lbl, fl) in enumerate(box.items()):
        p2 += (1 + h) * (slot + 1) * int(fl)
print(p2)
