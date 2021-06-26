"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import sys

sys.path.append('./bin/libs/')
sys.path.append('./')
import json5
import configparser
import decimal
import logging
import math
import time
import os
from xml.dom.minidom import parse

try:
    import configs
except ModuleNotFoundError:
    from bin import configs

# logger
tools_logger = logging.getLogger('part-tools')

"""
some tools
"""


def c_b(thing):  # stand for my bool
    yes = ['True', 'TRUE', 'true', '1', 1, True]
    no = ['False', 'FALSE', 'false', '0', 0, False]
    if thing in yes:
        return True
    elif thing in no:
        return False
    else:
        raise ValueError("Need a 'like bool' not anything else")


level_ = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL',
          logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]


def log_level(level):
    if level in level_:
        if (level == 'DEBUG') or (level == logging.DEBUG):
            return logging.DEBUG
        if (level == 'INFO') or (level == logging.INFO):
            return logging.INFO
        if (level == 'WARNING') or (level == logging.WARNING):
            return logging.WARNING
        if (level == 'ERROR') or (level == logging.ERROR):
            return logging.ERROR
        if (level == 'CRITICAL') or (level == logging.CRITICAL):
            return logging.CRITICAL
    else:
        raise ValueError('Need a like level thing not anything else')


# linear_algebra

def C_R_P(position, degrees):  # stand for calculation
    """
    very thanks for lenny from pyglet delvoper
    https://github.com/LennyPhoenix
    this part of code is write by him
    """
    radians = degrees * (math.pi / 180)
    cos = math.cos(radians)
    sin = math.sin(radians)
    rotated_pos = (position[0] * cos - position[1] * sin, position[0] * sin + position[1] * cos)
    return rotated_pos


"""
Physics calculation
"""


def is_decimal(A: any) -> bool:
    if type(A) is not type(decimal.Decimal):
        return False
    else:
        return True


def F_D(A: decimal, B: decimal) -> decimal:
    if is_decimal(A) and is_decimal(B):
        return A / B


def F_Mu(A: decimal, B: decimal) -> decimal:
    if is_decimal(A) and is_decimal(B):
        return A * B


def F_Mi(A: decimal, B: decimal) -> decimal:
    if is_decimal(A) and is_decimal(B):
        return A - B


def F_A(A: decimal, B: decimal) -> decimal:
    if is_decimal(A) and is_decimal(B):
        return A + B


def D_C(listA: list, listB: list) -> '1':  # stand for Duplicate check
    """
    usage:\n
    input two list\n
    the fun will do duplicate check and sort then\n
    the fun won't return any thing just change the list now
    """
    for unit in listB:
        if unit in listA:
            listA.remove(unit)
            listB.remove(unit)
        else:
            continue
    listA.sort()
    listB.sort()
    return 1


def S_C_float_check(SC):  # stand for Scientific notation's float check
    """
    formats:
    SC list format:docs.basic_config.json:basic_number"""
    while SC[0] >= 10:
        SC[0] = F_D(SC[0], 10)
        SC[1] += 1
    while SC[0] < 1:
        SC[0] = F_Mu(SC[0], 10)
        SC[1] -= 1


def S_N_M(*SN):  # stand for Scientific notation multiple
    """
    formats:
    A & B & C list format:docs.basic_config.json:basic_number"""
    if len(SN) < 2:
        raise TypeError('it need more than 2!')
    elif len(SN) == 2:
        return __S_N_M(SN[0], SN[1])
    else:
        R = __S_N_M(SN[0], SN[1])
        for A in SN[2:]:
            R = __S_N_M(R, A)
    return R


def __S_N_M(A, B):
    """
    formats:
    A & B list format:docs.basic_config.json:basic_number"""
    R = [F_Mu(A[0], B[0]), A[1] + B[1]]
    S_C_float_check(R)
    Unit1, Unit2 = A[2] + B[2], A[3] + B[3]
    if Unit1 is None:
        Unit1 = []
    D_C(Unit1, Unit2)
    R += [Unit1, Unit2]
    return R


def S_N_D(A, B):  # stand for Scientific notation divided
    """
    formats:
    A & B list format:docs.basic_config:basic_number"""
    R = [F_D(A[0], B[0]), A[1] - B[1]]
    S_C_float_check(R)
    Unit1, Unit2 = A[2] + B[3], A[3] + B[2]
    if Unit1 is None:
        Unit1 = []
    D_C(Unit1, Unit2)
    R += [Unit1, Unit2]
    return R


def G_C(M, m, R, G):  # stand for gravity calculation
    """
    formats:
    M : ship's mass
    m : planet's mass
    R : distance to the planet
    G : Gravitational constant
    M & m & R format: docs.basic_config:basic_number
    """
    g = configs.basic_force()
    A = S_N_M(M, m, G)
    g = S_N_D(A, S_N_M(R, R))
    return g


def distance(A, B):
    """
    formats:
    A & B format: docs.basic_config:basic_poi
    """
    poi_dis = configs.basic_poi()
    for x in A, B:
        x = decimal.Decimal(str(x))
    xd = A[0] - B[0]
    yd = A[1] - B[1]
    poi_dis[0] = xd
    poi_dis[1] = yd
    # 勾股定理
    poi_dis[0] **= 2
    poi_dis[1] **= 2
    poi_dis.append(poi_dis[0] + poi_dis[1])
    poi_dis[2] **= 0.5
    return poi_dis[2]


# loads


def config(file_name, stack=None):  # // TODO 加上.config的读取+解析
    f_type = file_name[file_name.rfind('.') + 1:]  # 从最后一个.到末尾 (截取文件格式)
    if (f_type == 'json5') or (f_type == 'json'):
        try:
            try:
                with open(file_name, 'r', encoding='utf-8') as jf:  # jf -> json file
                    rd = json5.load(jf)
            except UnicodeDecodeError:
                with open(file_name, 'r', encoding='gbk') as jf:
                    rd = json5.load(jf)
                tools_logger.info('文件 %s 解码错误，已重新使用gbk编码打开' % file_name)
        except FileNotFoundError as exp:
            log = 'no config json(5) file \n file name : %s \n stack : %s' % (
                file_name, stack)
            tools_logger.exception(log)
            raise FileNotFoundError(log)
        if stack is not None:
            rd = rd[stack]
        return rd
    elif f_type == 'xml':
        try:
            xml_load = parse(file_name)
        except FileNotFoundError as exp:
            log = 'no config xml file \n file name : %s \n stack : %s' % (
                file_name, stack)
            tools_logger.exception(log)
            raise FileNotFoundError(log)
        if stack is not None:
            xml_get = xml_load.getElementsByTagName(stack)
            return xml_get
        else:
            return xml_load
    elif (f_type == 'config') or (f_type == 'conf'):
        cp = configparser.ConfigParser()  # cp -> config parser
        cp.read(file_name)  # config parser -> reader


def get_At(name, in_xml, need_type=str):
    """
    get Attribute from a XML tree
    will raise TypeError if input is not str or list
    XML no!   Json5 yes!
    """
    name_type = type(name)
    if name_type == list:
        At_list = []
        for need_name in name:
            if in_xml.hasAttribute(need_name):
                get = in_xml.getAttribute(need_name)
                At_list.append(need_type(get))
            else:
                continue
        return At_list
    elif name_type == str:
        if in_xml.hasAttribute(name):
            At = in_xml.getAttribute(name)
        else:
            return None
    else:
        raise TypeError('only str and list type is ok but you give me a' + name_type + 'type')
    return need_type(At)


names = {'{time.time}': str(time.time()),
         '{dir}': str(os.getcwd()),
         '{py_v}': str(sys.version.split(' ')[0])}


def default_name_handler(name: str) -> str:
    """
    won't change the string
    just return one
    """
    name = name
    name = name.replace('{time.time}', str(time.time()))
    name = name.replace('{dir}', str(os.getcwd()))
    name = name.replace('{py_v}', str(sys.version.split(' ')[0]))
    return name


def name_handler(name: str, formats=None) -> str:
    if formats is None:
        return default_name_handler(name)
    name = default_name_handler(name)
    for need_replace in formats:
        replace = formats[need_replace]
        if need_replace == '{date}':
            replace = time.strftime(formats['{date}'], time.gmtime(time.time()))
        name = name.replace(need_replace, replace)
    return name
