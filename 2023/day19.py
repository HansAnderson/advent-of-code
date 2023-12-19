#!/usr/bin/env python3
import math
import operator
import pathlib
import re

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day19-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\n") for x in f]

example_1 = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
example_2 = """
in{x>0:ab,R}
ab{x<1:R,A}

{x=1,m=2,a=3,s=4}
"""
#lines = example_1[1:-1].split("\n")
#lines = example_2[1:-1].split("\n")

_W, _PR = [x.split("\n") for x in ("\n".join(lines)).split("\n\n")]

PR = [{k:int(v) for (k,v) in (x.split("=") for x in pr[1:-1].split(","))} for pr in _PR]
W = {n: [re.fullmatch(r"(([a-z]+)([<>])(-?\d+):)?([a-zAR]+)", r).groups()[1:] for r in rules[:-1].split(",")] for n, rules in (w.split("{") for w in _W)}

def make_rule(workflow):
    part, _op, _val, w = workflow
    if part is None:
        return lambda pr: w
    else:
        assert _op in ("<", ">")
        op = operator.lt if _op == "<" else operator.gt
        return lambda pr: w if op(pr[part], int(_val)) else None

W1 = {n: [make_rule(r) for r in rules] for n, rules in W.items()}

p1 = 0
for pr in PR:
    w = "in"
    while w not in ("A", "R"):
        for r in W1[w]:
            w = r(pr)
            if w is not None:
                break
    if w == "A":
        p1 += sum(pr.values())
print(p1)

PRP = {
    "x": (1,4000),
    "m": (1,4000),
    "a": (1,4000),
    "s": (1,4000),
}

def dfs(prp, w):
    if w == "A":
        return math.prod(l for s, l in prp.values())
    elif w == "R":
        return 0
    c = 0
    for p, op, _val, ww in W[w]:
        if p is not None:
            val = int(_val)
            s, l = prp[p]
            if (op == "<" and s >= val) or (op == ">" and s + l - 1 <= val):
                continue
            pprp = prp.copy()
            if op == "<" and s + l - 1 < val:
                prp[p] = (math.nan, 0)
            elif op == "<":
                prp[p] = (val, l - (val - s))
                pprp[p] = (s, val - s)
            elif op == ">" and s > val:
                prp[p] = (math.nan, 0)
            elif op == ">":
                prp[p] = (s, val + 1 - s)
                pprp[p] = (val + 1, l - (val + 1 - s))
            else:
                assert False, (p, op, val, ww, w, prp)
            c += dfs(pprp, ww)
        else:
            c += dfs(prp, ww)
    return c

print(dfs(PRP, "in"))
