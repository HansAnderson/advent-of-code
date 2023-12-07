#!/usr/bin/env python3
import collections
import functools
import pathlib

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day7-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
#lines = example_1[1:-1].split("\n")

# p1: 32t3k, ktjjt, kk677, t55j5, qqqja
# p2: 32t3k, kk677, t55j5, qqqja, ktjjt

hands = []
for line in lines:
    h, r = line.split()
    hands.append((h, int(r)))

def hand_type(h, is_part2=False):
    c = collections.Counter(h)
    # if all "J", leave hand alone
    if is_part2 and (num_j := c["J"]) != 5:
        c -= collections.Counter(J=num_j)
        c.update({c.most_common(1)[0][0]: num_j})
    mc = c.most_common()
    if mc[0][1] == 5:
        # five-of-a-kind
        return 6
    if mc[0][1] == 4:
        # four-of-a-kind
        return 5
    if mc[0][1] == 3 and mc[1][1] == 2:
        # full house
        return 4
    if mc[0][1] == 3:
        # three-of-a-kind
        return 3
    if mc[0][1] == 2 and mc[1][1] == 2:
        # two pair
        return 2
    if mc[0][1] == 2:
        # pair
        return 1
    return 0

def hand_cmp(h1, h2, is_part2=False):
    ht1 = hand_type(h1[0], is_part2)
    ht2 = hand_type(h2[0], is_part2)
    if ht1 < ht2:
        return -1
    if ht1 > ht2:
        return 1

    order = "AKQT98765432J" if is_part2 else "AKQJT98765432"

    for c1, c2 in zip(h1[0], h2[0]):
        if order.index(c1) > order.index(c2):
            return -1
        if order.index(c1) < order.index(c2):
            return 1
    assert False, f"{h1} and {h2} should not be equal"


hands.sort(key=functools.cmp_to_key(hand_cmp))
#print(hands)
p1 = 0
for i, (h, r) in enumerate(hands):
    p1 += (i + 1) * r
print(p1)

hands.sort(key=functools.cmp_to_key(functools.partial(hand_cmp, is_part2=True)))
#print(hands)
p2 = 0
for i, (h, r) in enumerate(hands):
    p2 += (i + 1) * r
print(p2)
