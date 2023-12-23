#!/usr/bin/env python3
import pathlib

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day23-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""
#lines = example_1[1:-1].split("\n")

X = len(lines[0])
Y = len(lines)
G = {(x, y): lines[y][x] for x in range(X) for y in range(Y)}
S = (1, 0)
E = (X-2, Y-1)

D = {
    ".": [(1, 0), (0, 1), (-1, 0), (0, -1)],
    ">": [(1, 0)],
    "v": [(0, 1)],
    "<": [(-1, 0)],
    "^": [(0, -1)],
}

q = [(0,S,set())]
p1 = 0
while q:
    l, (x, y), visited = q.pop(0)
    visited.add((x, y))
    if (x, y) == E:
        #print("...", l)
        p1 = max(p1, l)
    for dx, dy in D[G[x, y]]:
        xx = x + dx
        yy = y + dy
        if G.get((xx, yy)) in D.keys() and (xx, yy) not in visited:
            q.append((l + 1, (xx, yy), visited.copy()))
print(p1)

# compress maze into graph
V = {S:{}}
q = [((1, 1), [S])]
while q:
    (x, y), path = q.pop()
    opts = []
    for dx, dy in D["."]:
        xx = x + dx
        yy = y + dy
        if G.get((xx, yy)) in D.keys() and (xx, yy) != path[-1]:
            opts.append((xx, yy))
    if len(opts) == 1:
        path.append((x, y))
        q.append((opts[0], path))
    else:
        V[path[0]][x, y] = len(path)
        if (x, y) not in V:
            V[x, y] = {}
            for xx, yy in opts:
                q.append(((xx, yy), [(x, y)]))
        V[x, y][path[0]] = len(path)

q = [(0, S, set())]
p2 = 0
while q:
    l, v, visited = q.pop()
    visited.add(v)
    if v == E:
        p2 = max(p2, l)
        #print("...", l, p2)
    for vv, ll in V[v].items():
        if vv not in visited:
            q.append((l + ll, vv, visited.copy()))
print(p2)
