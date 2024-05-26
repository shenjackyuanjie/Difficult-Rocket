#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import os
import sys
import time
import math
import json
import tomli
import tomli_w
import configparser

from pathlib import Path
from typing import Union, Optional
from xml.etree import ElementTree
from defusedxml.ElementTree import parse

from Difficult_Rocket.exception.unsupport import NoMoreJson5

from lib_not_dr import loggers

# logger
tools_logger = loggers.config.get_logger("tools")
"""
file config
"""

file_error = {
    FileNotFoundError: "no {filetype} file was founded!:\n file name: {filename}\n file_type: {filetype}\n stack: {stack}",
    KeyError: "no stack in {filetype} file {filename} was found! \n file type: {} \n file name: {} \n stack: {stack}",
    Exception: "get some {error_type} when read {filetype} file {filename}! \n file type: {} \n file name: {} \n stack: {stack}",
}


def load_file(
    file_name: Union[str, Path],
    stack: Optional[Union[str, list, dict]] = None,
    raise_error: Optional[bool] = True,
    encoding: Optional[str] = "utf-8",
) -> Union[dict, ElementTree.ElementTree]:
    if isinstance(file_name, Path):
        file_name = str(file_name)
    f_type = file_name[file_name.rfind(".") + 1 :]  # 从最后一个.到末尾 (截取文件格式)
    get_file = NotImplementedError("解析失败，请检查文件类型/文件内容/文件是否存在！")
    try:
        if f_type == "xml":
            xml_load: ElementTree.ElementTree = parse(file_name)
            if stack is not None:
                get_file = xml_load.findall(stack)
        elif (f_type == "config") or (f_type == "conf") or (f_type == "ini"):
            get_file = configparser.ConfigParser()
            get_file.read(file_name)
            if stack:
                get_file = get_file[stack]
        elif f_type == "toml":
            with open(file_name, mode="rb") as file:
                get_file = tomli.load(file)
            if stack is not None:
                get_file = get_file[stack]
        elif f_type == "json":
            with open(file_name, mode="r", encoding=encoding) as file:
                get_file = json.load(file)
            if stack is not None:
                get_file = get_file[stack]
        elif f_type == "json5":
            raise NoMoreJson5("我说什么也不用json5了！喵的")
    except Exception as exp:
        error_type = type(exp)
        if error_type in file_error:
            tools_logger.error(
                file_error[error_type].format(
                    filetype=f_type, filename=file_name, stack=stack
                )
            )
        else:
            tools_logger.error(
                file_error[Exception].format(
                    error_type=error_type,
                    filetype=f_type,
                    filename=file_name,
                    stack=stack,
                )
            )
        if raise_error:
            raise exp from None
    return get_file


def save_dict_file(file_name: str, data: dict, encoding: str = "utf-8") -> bool:
    f_type = file_name[file_name.rfind(".") + 1 :]  # 从最后一个.到末尾 (截取文件格式)
    try:
        if (f_type == "config") or (f_type == "conf") or (f_type == "ini"):
            return False
        elif f_type == "toml":
            with open(file_name, mode="wb") as file:
                tomli_w.dump(data, file)
        elif f_type == "json":
            with open(file_name, mode="w", encoding=encoding) as file:
                json.dump(data, file)
        elif f_type == "json5":
            raise NoMoreJson5("我说什么也不用json5了！喵的")
    except Exception as exp:
        raise exp


# main config
main_config_file = load_file("./config/main.toml")


def get_At(name, in_xml, need_type=str):
    """
    get Attribute from a XML tree
    will raise TypeError if input is not str or list
    XML json5 no!   toml yes!
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
            attr = in_xml.getAttribute(name)
        else:
            return None
    else:
        raise TypeError(
            "only str and list type is ok but you give me a" + name_type + "type"
        )
    return need_type(attr)


def default_name_handler(name_: str) -> str:
    """
    won't change the string
    just return one
    """
    name = name_
    name = name.replace("{time.time}", str(time.time()))
    name = name.replace("{dir}", str(os.getcwd()))
    name = name.replace("{py_v}", str(sys.version.split(" ")[0]))
    name = name.replace("{version}", str(main_config_file["runtime"]["version"]))
    name = name.replace("{write_v}", str(main_config_file["runtime"]["write_py_v"]))
    return name


def name_handler(name: str, formats: dict = None) -> str:
    if formats is None:
        return default_name_handler(name)
    name = default_name_handler(name)
    for need_replace in formats:
        replace = formats[need_replace]
        if need_replace == "{date}":
            if "{date}" in formats:
                replace = time.strftime(formats["{date}"], time.gmtime(time.time()))
            else:
                replace = time.strftime(
                    main_config_file["runtime"]["date_fmt"], time.gmtime(time.time())
                )
        name = name.replace(need_replace, replace)
    return name


"""
some tools
"""

yes = ["true", "1", 1, 1.0, True]
no = ["false", "0", 0, 0.0, False, None]


def format_bool(thing) -> bool:
    """
    :param thing 啥都行，只要是能传进来的都可以

    如果看起来像"True" 比如 'true','1',1
    就返回 True
    如果看起来像"False" 比如 'false','0',0
    就返回 False
    都不像就 raise TypeError
    感谢来自MCDReforged的各位同志《你能在MCDR群里聊除了MCDR的任何东西》
    """
    if (thing in yes) or (isinstance(thing, str) and thing.lower() in yes):
        return True
    elif (thing in no) or (isinstance(thing, str) and thing.lower() in no):
        return False
    else:
        raise TypeError("Need a 'like bool' not a {}".format(thing))


# linear_algebra


def C_R_P(position, degrees):  # stand for calculation
    """
    very thanks for lenny from pyglet developer
    https://github.com/LennyPhoenix
    this part of code is write by him
    """
    radians = degrees * (math.pi / 180)
    cos = math.cos(radians)
    sin = math.sin(radians)
    rotated_pos = (
        position[0] * cos - position[1] * sin,
        position[0] * sin + position[1] * cos,
    )
    return rotated_pos
