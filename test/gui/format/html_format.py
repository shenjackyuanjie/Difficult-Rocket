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

import unittest

from Difficult_Rocket.client.guis.format import html

try_texts = [
    '明天天气很好',
    '从前有座山，山里有座庙, **is it**?',
    '啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊。阿巴巴巴',
    '阿瓦达达瓦的，aiwdhaihdwia.awdaiwhdahwido[12312](123131)',
    '1231231dawdawd65ewwe56er56*awdadad*aaa**阿伟大的阿瓦打我的**',
    'adwiuahiaa奥迪帮我auawuawdawdadw阿达达瓦aawd 2313',
    '阿松大阿瓦达达娃啊aawadaawdawd阿瓦达达娃'
]


class HtmlFormatTest(unittest.TestCase):
    def test1_format_texts(self):
        self.assertEqual(html.decode_text2HTML('明天天气很好'), '<font face="" color=white>明天天气很好</font>')


if __name__ == '__main__':
    unittest.main()
