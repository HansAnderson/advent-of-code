#!/usr/bin/env python3
import functools
import itertools
import math
import pathlib
import pprint

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day8-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
example_2 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
example_3 = """
LR

11A = (1QQ, XXX)
1QQ = (XXX, 2QQ)
2QQ = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
#lines = example_1[1:-1].split("\n")
#lines = example_2[1:-1].split("\n")
#lines = example_3[1:-1].split("\n")

instructions = lines[0]

network = {}
for line in lines[2:]:
    node, next_ = line.split(" = ")
    network[node] = next_[1:-1].split(", ")

#pprint.pprint(network)

p1 = 0
node = "AAA"
for inst in itertools.cycle(instructions):
    node = network[node][0 if inst == "L" else 1]
    p1 += 1
    if node == "ZZZ":
        break
print(f"part1: {p1}")

wip_nodes = [[(x, -1)] for x in network.keys() if x.endswith("A")]
nodes = []
for step, inst in itertools.cycle(enumerate(instructions)):
    for i in range(len(wip_nodes)-1, -1, -1):
        steps = wip_nodes[i]
        node = steps[-1][0]
        next_step = (network[node][0 if inst == "L" else 1], step)
        if next_step[0].endswith("Z") and next_step in steps:
            del wip_nodes[i]
            nodes.append([steps, next_step])
        else:
            steps.append(next_step)
    if not wip_nodes:
        break

#pprint.pprint(nodes)
cycle_lens = []
for i, (steps, next_step) in enumerate(nodes):
    if len(lines) < 100:
        print(steps)
    cycle_start = steps.index(next_step)
    nodes[i].append(cycle_start)
    cycle_len = len(steps) - cycle_start
    nodes[i].append(cycle_len)
    nz = 0
    for node, _ in steps:
        if node.endswith("Z"):
            nz += 1
    print(f"total {len(steps)}, start {cycle_start}, len {cycle_len}, z's {nz}")

    cycle_lens.append(cycle_len)

def lcm(denominators):
    return functools.reduce(lambda a,b: a*b // math.gcd(a,b), denominators)

cycle_lcm = lcm(cycle_lens)
print(f"LCM: {cycle_lcm}")

p2 = nodes[-1][2]
step_size = nodes[-1][3]
found = False
while not found:
    p2 += step_size
    if p2 < cycle_lcm:
        # taking too long... skip until first LCM?
        continue
    print(f"checking {p2}")
    found = True
    for steps, _, cycle_start, cycle_len in nodes:
        cand = steps[((p2 - cycle_start) % cycle_len) + cycle_start][0]
        #print(f"  {cand}")
        if not cand.endswith("Z"):
            found = False
            break
print(f"part2: {p2}")

# WHAT?!?!? the first match is the LCM... I don't understand :(
