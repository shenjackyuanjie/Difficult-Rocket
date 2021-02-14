
import json5
import pprint


with open('configs/view.json5') as view:
    a = view.read()
    pprint.pprint(a)