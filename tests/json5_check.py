import pprint

with open('sys_value/parts.json5', 'r+', encoding='utf-8') as view:
    a = view.read()
    pprint.pprint(a)
