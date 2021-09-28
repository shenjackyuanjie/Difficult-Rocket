#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

from Difficult_Rocket.api import tools
import os

import PIL.Image
import json5


def rewrite_config(name, save_name):
    load_xml = tools.load_file(name)
    load_xml = load_xml.documentElement
    sprites = load_xml.getElementsByTagName('sprite')
    pic_path = load_xml.getAttribute('imagePath')
    poise = {'image_name': pic_path, 'images': {}}
    for sprite in sprites:
        poi = tools.get_At(['x', 'y', 'w', 'h'], sprite, int)
        poi.append(tools.get_At('r', sprite, str))
        save_image = tools.get_At('n', sprite, str)
        if save_image.find('PNG') != -1:
            save_image = save_image[:-3] + 'png'
        poise['images'][save_image] = poi
    with open(save_name, 'w') as file:
        json5.dump(poise, file)


def cut_and_save(config, save_path):
    with open(config) as con:
        configs = json5.load(con)
    pic = PIL.Image.open('textures/' + configs['image_name'])
    try:
        os.mkdir('textures/' + save_path)
    except Exception as exp:
        print(exp)
    for config_ in configs['images']:
        config__ = configs['images'][config_]
        save_name = 'textures/%s/%s' % (save_path, config_)
        x, y, w, h, t = config__[0], config__[1], config__[2], config__[3], config__[4]
        crop_box = [x, y, x + w, y + h]
        pic_ = pic.crop(crop_box)
        if t == 'y':
            pic_ = pic_.rotate(90, expand=True)
        print(save_name)
        pic_.save(save_name)


def All_in_one_cut(xml, path):
    json_name = xml[:-4] + '.json5'
    rewrite_config(xml, json_name)
    cut_and_save(json_name, path)
