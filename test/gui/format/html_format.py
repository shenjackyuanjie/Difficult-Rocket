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

import os
import cProfile

os.chdir('..')
os.chdir('..')
os.chdir('..')


from Difficult_Rocket.guis.format import html

try_texts = [
    '明天天气很好',
    '从前有座山，山里有座庙, **is it**?',
    '啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊。阿巴巴巴',
    '阿瓦达达瓦的，aiwdhaihdwia.awdaiwhdahwido[12312](123131)',
    '1231231dawdawd65ewwe56er56*awdadad*aaa**阿伟大的阿瓦打我的**',
    'adwiuahiaa奥迪帮我auawuawdawdadw阿达达瓦aawd 2313',
    '阿松大阿瓦达达娃啊aawadaawdawd阿瓦达达娃'
]


def main_test():
    for text in try_texts:
        print(text)
        print(html.decode_text2HTML(text))
        print('------')


check = True
if check:
    cProfile.run('main_test()', sort='calls')
else:
    main_test()
