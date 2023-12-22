#!/usr/bin/env python3
import collections
import pathlib

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day22-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""
#lines = example_1[1:-1].split("\n")

R = []
for line in lines:
    r = [p.split(",") for p in line.split("~")]
    r[0] = [int(x) for x in r[0]]
    r[1] = [int(x) for x in r[1]]
    assert r[0][2] <= r[1][2]
    R.append(r)

# sort blocks by z
R.sort(key=lambda x: x[0][2])

# for each (x,y), keep track of current z and which block occupies that cube
floor = collections.defaultdict(lambda: (0, None))
# block x "supports" block y
supports = collections.defaultdict(set)
# block y is "supported_by" block x
supported_by = collections.defaultdict(set)

for i, ((x1,y1,z1), (x2,y2,z2)) in enumerate(R):
    # find min z where next block can drop to
    z = 0
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            z = max(z, floor[x, y][0])
    R[i] = (x1, y1, z+1), (x2, y2, z+1+(z2-z1))

    # find supporting blocks
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            z, j = floor[x, y]
            if R[i][1][2] > z:
                # raise floor
                floor[x,y] = R[i][1][2], i
                # any block with cube at z-1 supports this block
                if R[i][0][2] == z + 1 and j is not None:
                    supports[j].add(i)
                    supported_by[i].add(j)

# how many blocks don't support other blocks
p1 = sum(all(len(supported_by[y]) > 1 for y in supports[i]) for i in range(len(R)))
print(p1)

# sum of blocks that would fall if each block were removed
p2 = 0
for i in range(len(R)):
    fallen = set()
    q = [i]
    while q:
        y = q.pop(0)
        fallen.add(y)
        for z in supports[y]:
            if len(supported_by[z] - fallen) == 0 and z not in fallen:
                q.append(z)
    p2 += len(fallen) - 1
print(p2)
