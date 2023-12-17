#!/usr/bin/env python3
import copy
import heapq
import pathlib

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day17-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""
example_2 = """
111111111111
999999999991
999999999991
999999999991
999999999991
"""
#lines = example_1[1:-1].split("\n")
#lines = example_2[1:-1].split("\n")

G = [[int(x) for x in y] for y in lines]
Y = len(lines)
X = len(lines[0])
# heat loss, (x, y), (dx, dy, steps), path
S = (0, (0, 0), (1, 0, 0), [])
E = (X-1, Y-1)

R = {
    (1, 0): (0, 1),
    (0, 1): (-1, 0),
    (-1, 0): (0, -1),
    (0, -1): (1, 0),
}
L = {
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
}

D = {
    (1, 0): ">",
    (0, 1): "v",
    (-1, 0): "<",
    (0, -1): "^",
}

def add_if_valid(states, known, hl, x, y, dx, dy, ss, path):
    xx = x + dx
    yy = y + dy
    if 0 <= xx < X and 0 <= yy < Y and (xx, yy):
        new_hl = hl + G[yy][xx]
        k = (x, y, dx, dy, ss)
        if k not in known:
            known.add(k)
            heapq.heappush(states, (new_hl, (xx, yy), (dx, dy, ss), path))

def run(min_step, max_step):
    states = [S]
    known = set()

    while states:
        state = heapq.heappop(states)
        hl, (x, y), (dx, dy, ss), path = state
        if 0:
            path = path.copy() + [(x, y, D[dx, dy])]
            print(state)
            _G = copy.deepcopy(G)
            for _x, _y, _d in path:
                _G[_y][_x] = _d
            print("\n".join("".join(str(c) for c in l) for l in _G))
        if (x, y) == E and ss >= min_step:
            return hl
        if ss < max_step:
            add_if_valid(states, known, hl, x, y, dx, dy, ss + 1, path)
        if ss >= min_step:
            add_if_valid(states, known, hl, x, y, *R[(dx, dy)], 1, path)
            add_if_valid(states, known, hl, x, y, *L[(dx, dy)], 1, path)

p1 = run(1, 3)
print(p1)

p2 = run(4, 10)
print(p2)
