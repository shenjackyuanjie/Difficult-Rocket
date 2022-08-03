import os

os.system('')

reset = '\033[0m'

print('A 000')

do = False


def rgb(r, g, b):
    return 2, r, g, b


i_list = list(range(30, 39, 1))
# i_list = [39]
j_list = list(range(40, 49, 1))
# j_list = [49]

for i in i_list:
    for j in j_list:
        print(f'\033[{i};{j}m{i}|{j} {reset}', end='|')
    print()
print()


def color_print(*args):
    args = [str(i) for i in args]
    out = '|'.join(args)
    line = ';'.join(args)
    print(f'\033[{line}m{out}\033[0m')


reset_color = '\033[0m'

# exit(0)

color_print(94)
color_print(41, 93)
color_print(36, 40)
print()
color_print(48, *rgb(200, 100, 20), 34)
color_print(48, *rgb(255, 161, 72))
color_print(48, *rgb(255, 161, 72), 38, *rgb(1, 50, 255))
color_print(48, *rgb(178, 112, 50), 38, *rgb(98, 96, 167))
print()
color_print(48, *rgb(120, 10, 10), 38, *rgb(50, 100, 110))

color_print(34, 40)
color_print(32, 40)
print('trace: ', end='')
color_print(48, *rgb(40, 40, 40))
print('some trace', reset_color)

print('fine: ', end='')
color_print(35)
print('some fine', reset_color)

print('debug: ', end='')
color_print(38, *rgb(133, 138, 149))
print('some debug', reset_color)

print('info: ', end='')
color_print(0)
print('some info', reset_color)

print('warn: ', end='')
# color_print(31, 48, *rgb(56, 28, 0))
color_print(33)
print('some warn', reset_color)

print('error: ', end='')
color_print(31)
print('some error', reset_color)

print('fatal: ', end='')
color_print(33, 41)
print('some fatal', reset_color)
