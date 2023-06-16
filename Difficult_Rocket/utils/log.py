#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import logging

from typing import Callable


__all__ = [
    'get_named_client_logger',
    'get_named_server_logger',
    'get_named_main_logger',
]


def _gen_get_named_logger(from_name: str) -> Callable[[str], logging.Logger]:

    def get_named_logger(name: str) -> logging.Logger:
        logger = logging.getLogger(from_name)
        logger.name = f'{from_name}.{name}'
        return logger

    return get_named_logger


get_named_client_logger = _gen_get_named_logger('client')
# 用于获取一个基于 client 配置的 logger
get_named_server_logger = _gen_get_named_logger('server')
# 用于获取一个基于 server 配置的 logger
get_named_main_logger = _gen_get_named_logger('main')
# 用于获取一个基于 main 配置的 logger
