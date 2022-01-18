#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import re
import pprint

from Difficult_Rocket import translate


default_style = {
    'font_name': 'Times New Roman',
    'font_size': 12,
    'bold': False,
    'italic': False
}



class SingleTextStyle:
    """
    单个字符的字体样式
    """

    def __init__(self,
                 font_name: str = '',
                 font_size: int = 12,
                 bold: bool = False,
                 italic: bool = False,
                 color: str = 'white',
                 text_tag: list = None,
                 show: bool = True,
                 prefix: str = '',
                 suffix: str = '',
                 text: str = ''):
        self.font_name = font_name
        self.font_size = font_size
        self.bold = bold
        self.italic = italic
        self.color = color
        self.prefix = prefix
        self.suffix = suffix

        if not text_tag:
            self._tag = []
        else:
            self._tag = text_tag
        self.show = show
        self.text = text

    @property
    def tag(self) -> list:
        return self._tag

    @tag.setter
    def tag(self, value: list):
        assert type(value) == list, 'SingleTextStyle.tag must be list'
        for tag in value:
            if tag not in self._tag:
                self._tag.append(tag)
        self._tag.sort()

    """
    对运算操作的支持
    """

    def __add__(self, other: 'SingleTextStyle') -> 'SingleTextStyle':
        """
        叠加两个字体样式 优先使用 other 的样式
        :param other: 叠加的字体样式
        :return: 叠加后的字体样式
        """
        assert type(other) == SingleTextStyle, f'SingleTextStyle + other\n other must be the same type, not a {type(other)}'
        return SingleTextStyle(
                font_name=other.font_name or self.font_name,
                font_size=other.font_size or self.font_size,
                bold=other.bold or self.bold,
                italic=other.italic or self.italic,
                color=other.color or self.color,
                text_tag=other.tag + self.tag,
                show=other.show or self.show,
                prefix=other.prefix + self.prefix,
                suffix=other.suffix + self.suffix,
                text=self.text
        )

    def __iadd__(self, other: 'SingleTextStyle') -> 'SingleTextStyle':
        """
        叠加两个字体样式 优先使用 other 的样式
        :param other: 叠加的字体样式
        :return: 叠加后的字体样式
        """
        assert type(other) == SingleTextStyle, f'SingleTextStyle += other\n other must be the same type, not a {type(other)}'
        self.font_name = other.font_name or self.font_name
        self.font_size = other.font_size or self.font_size
        self.bold = other.bold or self.bold
        self.italic = other.italic or self.italic
        self.color = other.color or self.color
        self.tag += other.tag
        self.show = other.show or self.show
        self.prefix += other.prefix
        self.suffix += other.suffix
        self.text = self.text
        return self

    """
    对各种判定的支持
    """

    def have_tag(self, other: 'SingleTextStyle') -> bool:
        """
        比较两个字体样式tag是否相同
        :param other: 叠加的字体样式
        :return: 是否相同
        """
        assert type(other) == SingleTextStyle
        return other.tag in self.tag

    def same_font(self, other: 'SingleTextStyle') -> bool:
        """
        比较两个字体样式的字体属性是否相同
        :param other: 叠加的字体样式
        :return: 是否相同
        """
        assert type(other) == SingleTextStyle
        return (self.font_name == other.font_name and
                self.font_size == other.font_size and
                self.color == other.color and
                self.show == other.show)

    def same_bold(self, other: 'SingleTextStyle') -> bool:
        """
        比较两个字体样式的加粗属性是否相同
        :param other: 叠加的字体样式
        :return: 是否相同
        """
        assert type(other) == SingleTextStyle
        return self.bold == other.bold

    def same_italic(self, other: 'SingleTextStyle') -> bool:
        """
        比较两个字体样式的斜体属性是否相同
        :param other: 叠加的字体样式
        :return: 是否相同
        """
        assert type(other) == SingleTextStyle
        return self.italic == other.italic

    """
    自动输出一些属性的支持
    """

    def HTML_font(self, suffix: bool = False) -> str:
        """
        输出字体样式的HTML字符
        :return: HTML 格式字符
        """
        if suffix:
            return font_HTML_end
        text = f'<font face="{self.font_name}" color={self.color}'
        if self.font_size != default_style['font_size']:
            text += f' real_size={self.font_size}'
        text += '>'
        return text

    def HTML_bold(self, suffix: bool = False) -> str:
        """
        输出字体粗体的HTML字符
        :return: HTML 格式字符
        """

        if self.bold:
            if suffix:
                return bold_HTML_end
            return '<b>'
        else:
            return ''

    def HTML_italic(self, suffix: bool = False) -> str:
        """
        输出字体斜体的HTML字符
        :return: HTML 格式字符
        """
        if self.italic:
            if suffix:
                return italic_HTML_end
            return '<i>'
        else:
            return ''

    def HTML(self, suffix: bool = False) -> str:
        """
        输出字体样式的HTML字符
        :return: HTML 格式字符
        """
        if not suffix:
            return self.HTML_bold() + self.HTML_italic() + self.HTML_font()
        else:
            return font_HTML_end + (bold_HTML_end if self.bold else '') + (italic_HTML_end if self.italic else '')


# [\u4e00-\u9fa5] 中文字符
default_fonts_config = [
    {
        'match': re.compile(r'.'),  # 匹配的字符  匹配选项是re.compile()
        'shown': re.compile(r'.'),  # 匹配到的字符中显示的部分  匹配选项是re.compile()
        'style': SingleTextStyle(font_name=translate.鸿蒙简体, font_size=15, bold=False, italic=False, show=True, color='white'),
    },
    {
        'match': re.compile(r'[a-zA-Z0-9]'),
        'shown': re.compile(r'[a-zA-Z0-9]'),
        'style': SingleTextStyle(font_name=translate.微软等宽, font_size=15)
    },
    # Markdown 语法规则匹配
    {
        # Markdown 粗体语法规则匹配
        'match': re.compile(r'\*\*(.*?(?<!\s))\*\*'),
        'shown': re.compile(r'(?<=\*\*)(.*?(?<!\s))(?=\*\*)'),
        'tag':   {
            # 为 match 匹配到的字符添加标签
            'match': re.compile(r'\*\*'),
            'style': SingleTextStyle(text_tag=['bold'])
        },
        'style': SingleTextStyle(bold=True)
    },
    {
        # Markdown 斜体语法规则匹配
        'match':  re.compile(r'\*(.*?(?<!\s))\*'),
        'shown':  re.compile(r'(?<=\*)(.*?(?<!\s))(?=\*)'),
        'ignore': {
            # 如果匹配到的字符含有 tag 就忽略本次解析
            'match': re.compile(r'\*'),
            'tag':   SingleTextStyle(text_tag=['italic'])
        },
        'style':  SingleTextStyle(italic=True)
    },
    {
        # Markdown 链接规则匹配
        # 注意：这里的匹配模式是非贪婪的，即匹配到的结果必须是完整的
        # 即：链接名称不能是空格等空白字符开头，链接名称不能是空格等空白字符结尾
        # 匹配的内容：[abc](def)
        # 显示的内容：abc
        'match': re.compile(r'\[(.*?(?<!\s))\]\((.*?(?<!\s))\)'),
        'shown': re.compile(r'(?<=\[)(.*?(?<!\s))(?=\]\((.*?(?<!\s))\))'),
        'style': SingleTextStyle(bold=True)
    }
]
font_HTML_end = '</font>'
bold_HTML = '<b>'
bold_HTML_end = '</b>'
italic_HTML = '<i>'
italic_HTML_end = '</i>'


def decode_text2HTML(text: str,
                     configs=None) -> str:
    if text == '':
        return ''
    if configs is None:
        configs = default_fonts_config
    style_list = [SingleTextStyle(text=text[x]) for x in range(0, len(text))]

    # 根据输入的配置对每一个字符进行样式设定
    for config in configs:
        # 根据 配置"文件"
        match_texts = config['match'].finditer(text)  # 使用config.match匹配
        for match_text in match_texts:  # 每一个匹配到的匹配项
            text_match = match_text.group()  # 缓存一下匹配到的字符，用于匹配显示的字符
            shown_texts = config['shown'].finditer(text_match)  # 使用config.shown匹配
            match_start, match_end = match_text.span()

            if 'ignore' in config:  # 如果样式选项包含忽略某些字符的tag
                ignore_texts = config['ignore']['match'].finditer(text_match)  # 根据选项匹配可能忽略的字符
                ignore = False  # 忽略先为False
                for ignore_text in ignore_texts:  # 每一个可能忽略的字符
                    if ignore:  # 为了方便退出
                        break
                    for ignore_index in range(match_start + ignore_text.span()[0], match_start + ignore_text.span()[1]):  # 对每一个可能的字符进行检测
                        if style_list[ignore_index].have_tag(config['ignore']['tag']):  # 如果确实包含要忽略的
                            ignore = True  # 忽略为True
                            break
                if ignore:
                    continue  # 跳过本次匹配

            if 'tag' in config:  # 如果样式选项包含对部分字符添加tag
                tag_texts = config['tag']['match'].finditer(text_match)  # 根据配置的正则表达式匹配要添加tag的字符
                for tag_text in tag_texts:  # 对每一个匹配到的~~~~~~
                    for tag_index in range(match_start + tag_text.span()[0], match_start + tag_text.span()[1]):  # 用于遍历匹配到的字符
                        style_list[tag_index] += config['tag']['style']

            # 为匹配到的字符添加样式
            for match_index in range(match_start, match_end):  # 用于遍历匹配到的字符
                # 这里用match index来精确读写列表里的元素，毕竟re.Match返回的span是两个标点，得遍历
                style_list[match_index] += config['style']  # 字体样式列表的[match_index] += config['style']的样式
                style_list[match_index].show = False  # 设置显示属性变为False

            # 为每一个显示的字符设置显示属性
            for shown_text in shown_texts:  # 每一个显示的匹配项
                for shown_index in range(match_start + shown_text.span()[0], match_start + shown_text.span()[1]):
                    style_list[shown_index].show = True
                    # 字体样式列表的[shown_index]设置显示属性变为True

    # 开始根据配置好的样式输出HTML文本
    style_list[0].prefix += style_list[0].HTML()  # 不管怎么说都要在最前面加一个字符标识
    for style_index in range(1, len(style_list)):
        if style_list[style_index].show:  # 如果这个字符显示
            if not style_list[style_index - 1].show:  # 如果前面一个字符不显示(且这个字符显示)
                style_list[style_index].prefix += style_list[style_index].HTML()  # 那么就直接给这个字符的前缀添加
            else:  # 开始根据前面的情况处理每种单独的标签
                if not style_list[style_index - 1].same_font(style_list[style_index]):
                    style_list[style_index - 1].suffix += style_list[style_index - 1].HTML_font(suffix=True)
                    style_list[style_index].prefix += style_list[style_index].HTML_font()
                if not style_list[style_index - 1].same_bold(style_list[style_index]):
                    style_list[style_index - 1].suffix += style_list[style_index - 1].HTML_bold(suffix=True)
                    style_list[style_index].prefix += style_list[style_index].HTML_bold()
                if not style_list[style_index - 1].same_italic(style_list[style_index]):
                    style_list[style_index - 1].suffix += style_list[style_index - 1].HTML_italic(suffix=True)
                    style_list[style_index].prefix += style_list[style_index].HTML_italic()
        else:  # 如果这个字符不显示
            if style_list[style_index - 1].show:  # 如果前面一个字符显示(且这个字符不显示)
                style_list[style_index - 1].suffix += style_list[style_index - 1].HTML(suffix=True)
            # 如果前面一个字符也不显示那就直接pass
    if style_list[-1].show:
        style_list[-1].suffix += style_list[-1].HTML(suffix=True)

    # 输出最终的HTML文本
    formatted_HTML_text = ''  # 初始化一下
    for style in style_list:  # 每一个样式
        if style.show:  # 如果这个字符显示
            formatted_HTML_text += style.prefix + style.text + style.suffix  # 文本的后面附加一下
    del style_list  # 主动删掉style_list 释放内存
    return formatted_HTML_text  # 返回，DONE！
