import configparser

configs = configparser.ConfigParser()

configs.read('test_config.config')

# print(configs.sections())
back = {}
for c in configs.sections():
    back[c] = {}
    for con in configs[c]:
        back[c][con] = configs[c][c]
        # name = configs[c][con]
        # print(c, con, name)
print('ree')
b = {}
for c in configs:
    print(c)
    b[c] = configs[c]
# print(configs['a'])
print('ree')
conf = configparser.ConfigParser()
# conf.read('test_config.config')
# print(type(conf))
print(back)
print(b)
