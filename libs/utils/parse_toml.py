import json
import pprint
import sys

import tomlkit as toml

with open(sys.argv[1], encoding="utf-8", mode="r") as f:
    if sys.argv[2] == "parse":
        a = toml.load(f)
        b = json.dumps(a)
        print(b)
    else:
        a = json.load(f)
    print(a)
    pprint.pprint(a, width=100)
