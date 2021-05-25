import configparser

configs = configparser.ConfigParser()

configs.read('test_config.config')

print(configs.sections())
for c in configs.sections():
    for con in configs[c]:
        name = configs[c][con]
        print(c, con, name)

conf = configparser.ConfigParser()
conf.read('test_config.config')
print(type(conf))