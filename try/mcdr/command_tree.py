#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

from mcdreforged.api.command import *

test_command_tree = Literal('!!test')

test_command_tree.parse('aaaaa')
