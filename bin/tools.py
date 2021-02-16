'''
writen by shenjackyuanjie
mail: 3695888@qq.com
'''

import re
import json5
import decimal
import logging
from xml.dom.minidom import parse

try:
    import configs
except ModuleNotFoundError:
    from bin import configs

# logger
tools_logger = logging.getLogger('tools')

'''
some tools
'''


def c_b(thing):  # stand for my bool
    yes = ['True', 'TRUE', 'true', '1', 1, True]
    no = ['False', 'FALSE', 'false', '0', 0, False]
    if thing in yes:
        return True
    elif thing in no:
        return False
    else:
        raise ValueError("Need a 'like bool' not anything else")


def log_level(level):
    level_ = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', logging.DEBUG,
              logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
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


'''
Physics calculation
'''


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
    '''
    usage:\n
    input two list\n
    the fun will do duplicate check and sort then\n
    the fun won't return any thing just change the list now
    '''
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
    '''
    formats:
    SC list format:docs.basic_config.json:basic_number'''
    while SC[0] >= 10:
        SC[0] = F_D(SC[0], 10)
        SC[1] += 1
    while SC[0] < 1:
        SC[0] = F_Mu(SC[0], 10)
        SC[1] -= 1


def S_N_M(*SN):  # stand for Scientific notation multiple
    '''
    formats:
    A & B & C list format:docs.basic_config.json:basic_number'''
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
    '''
    formats:
    A & B list format:docs.basic_config.json:basic_number'''
    R = [F_Mu(A[0], B[0]), A[1] + B[1]]
    S_C_float_check(R)
    Unit1, Unit2 = A[2] + B[2], A[3] + B[3]
    if Unit1 is None:
        Unit1 = []
    D_C(Unit1, Unit2)
    R += [Unit1, Unit2]
    return R


def S_N_D(A, B):  # stand for Scientific notation divided
    '''
    formats:
    A & B list format:docs.basic_config:basic_number'''
    R = [F_D(A[0], B[0]), A[1] - B[1]]
    S_C_float_check(R)
    Unit1, Unit2 = A[2] + B[3], A[3] + B[2]
    if Unit1 is None:
        Unit1 = []
    D_C(Unit1, Unit2)
    R += [Unit1, Unit2]
    return R


def G_C(M, m, R, G):  # stand for gravity calculation
    '''
    formats:
    M : ship's mass
    m : planet's mass
    R : distance to the planet
    G : Gravitational constant
    M & m & R format: docs.basic_config:basic_number
    '''
    g = configs.basic_force()
    A = S_N_M(M, m, G)
    g = S_N_D(A, S_N_M(R, R))
    return g


def distance(A, B):
    '''
    formats:
    A & B format: docs.basic_config:basic_poi
    '''
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


def config(file_name, stack=None):
    type = file_name[file_name.rfind('.') + 1:]  # 从最后一个.到末尾 (截取文件格式)
    if (type == 'json5') or (type == 'json'):
        try:
            with open(file_name, 'r', encoding='utf-8') as jf:  # jf -> json file
                rd = json5.load(jf)
        except FileNotFoundError as exp:
            log = 'no config json(5) file \n file name : %s \n stack : %s' % (
                file_name, stack)
            tools_logger.exception(log)
            raise FileNotFoundError(log)
        if stack is not None:
            rd = rd[stack]
        return rd
    elif type == 'xml':
        try:
            xml_load = parse(file_name)
        except FileNotFoundError as exp:
            log = 'no config json(5) file \n file name : %s \n stack : %s' % (
                file_name, stack)
            tools_logger.exception(log)
            raise FileNotFoundError(log)
        if stack is not None:
            xml_get = xml_load.getElementsByTagName(stack)
            return xml_get
        else:
            return xml_load


def get_At(name, in_xml, need_type=str):
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
