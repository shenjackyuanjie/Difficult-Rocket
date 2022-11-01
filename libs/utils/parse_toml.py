import json
import pprint
import sys

import tomlkit

with open(sys.argv[1], encoding='utf-8', mode='r') as f:
    if sys.argv[2] == 'parse':
        a = tomlkit.load(f)
    else:
        a = json.load(f)
    print(a)
    pprint.pprint(a, width=100)
