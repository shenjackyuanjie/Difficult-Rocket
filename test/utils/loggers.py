#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import unittest
# from libs.utils.build import logger as c_logger
from trytry.c.logger import logger as py_logger


class LoggerTest(unittest.TestCase):
    def check_a_logger(self, logger: py_logger.Logger, config: dict):
        self.assertEqual(logger.trace('aaaa trace'), config)
        logger.fine('ruaaa fine')
        logger.debug()

    def test_1_py_logger(self):
        ...

    # def test_2_c_logger(self):
    #     ...
