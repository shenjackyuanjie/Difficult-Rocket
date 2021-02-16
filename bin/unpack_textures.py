"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

try:
    from bin import tools
except (ModuleNotFoundError, ImportError, ImportWarning):
    import tools
import json5
from pprint import pprint
from pyglet import image


def rewrite_config(name, save_name):
    load_xml = tools.config(name)
    load_xml = load_xml.documentElement
    sprites = load_xml.getElementsByTagName('sprite')
    pic_path = load_xml.getAttribute('imagePath')
    poise = {'image_name': pic_path}
    for sprite in sprites:
        poi = tools.get_At(['x', 'y', 'w', 'h'], sprite, int)
        poi.append(tools.get_At('r', sprite, str))
        poise[tools.get_At('n', sprite, str)] = poi
    with open(save_name, 'w') as file:
        json5.dump(poise, file)


def cut_and_save(config):
    with open(config, 'r') as cut:
        cuts = json5.load(cut)
    main = image.load()


rewrite_config('textures/Runtime.xml', 'textures/Runtime.json5')
