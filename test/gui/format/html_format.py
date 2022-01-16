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
    '明天天气很好',
    '从前有座山，山里有座庙, **is it**?'
]

for text in try_texts:
    print(text)
    print(html.decode_text2HTML(text))
    print('------')
