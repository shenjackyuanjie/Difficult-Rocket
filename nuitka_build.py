#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import subprocess
from libs.utils import nuitka

if __name__ == '__main__':
    compiler = nuitka.Status()

    print(compiler)

    print(compiler.gen_subprocess_cmd())

