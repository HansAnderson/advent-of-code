#!/usr/bin/env python3
import datetime
import pathlib
import pytz
import requests
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

py_template = '''\
#!/usr/bin/env python3
import collections
import copy
import functools
import heapq
import itertools
import math
#import numpy as np
import operator
import pathlib
import pprint
import re
import sys

input_path = pathlib.Path(__file__).resolve().parent.joinpath("day{day}-input.txt")
with input_path.open("r") as f:
    lines = [x.rstrip("\\n") for x in f]

example_1 = """
"""
lines = example_1[1:-1].split("\\n")

# re-group lines in double-newline splits
#groups = [x.split("\\n") for x in ("\\n".join(lines)).split("\\n\\n")]

# extract numbers
#for line in lines:
#    nums = (int(x) for x in re.findall(r"-?\d+", line))

# extract overlap patterns
#for line in lines:
#    items = list(re.findall(r"(?=(aba|121))", line))
'''

token_path = pathlib.Path("aoc-session-token.txt")
if token_path.exists():
    with token_path.open("r") as f:
        aoc_session_token = f.read().strip()
else:
    eprint(f"Missing AoC session token '{token_path}'")
    sys.exit(1)

est_date = datetime.datetime.now(pytz.timezone("US/Eastern")).date()
if est_date.month != 12:
    eprint("Slow down there Santa. It's not even December!")
    sys.exit(1)
aoc_day = (est_date - est_date.replace(day=1)).days + 1
print(f"AoC {est_date.year} day {aoc_day}")

aoc_input_path = pathlib.Path(f"{est_date.year}/day{aoc_day}-input.txt")
if aoc_input_path.exists():
    print(f"{aoc_input_path} already downloaded")
else:
    session = requests.Session()
    session.cookies.set("session", aoc_session_token)
    rsp = session.get(f"https://adventofcode.com/{est_date.year}/day/{aoc_day}/input")
    if rsp.status_code == 200:
        with aoc_input_path.open("w") as f:
            f.write(rsp.text)
    elif rsp.status_code == 400:
        # bad session token?
        eprint(f"Auth error: {rsp.text}")
        sys.exit(1)
    else:
        eprint(f"{rsp.status_code}: {rsp.text}")
        sys.exit(1)

aoc_py_path = pathlib.Path(f"{est_date.year}/day{aoc_day}.py")
if aoc_py_path.exists():
    print(f"{aoc_py_path} already generated")
else:
    with aoc_py_path.open("w") as f:
        f.write(py_template.format(day=aoc_day))
    aoc_py_path.chmod(0o755)
