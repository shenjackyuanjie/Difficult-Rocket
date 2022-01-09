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

import re
import os
import parse

os.chdir('..')
os.chdir('..')
os.chdir('..')

from Difficult_Rocket.guis.format import html

try_texts = [
    'abcaaaa啊啊啊啊',
    '从前*有座*山~',
    '**挼**aaaaa[awda](123123)',
    '[aaaa](嗷嗷喊)'
]

for text in try_texts:
    print(text)
    print(html.decode_text2HTML(text))
    print('------')
