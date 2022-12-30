#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys

sys.path.append(os.path.abspath(os.curdir))
if '-env' not in sys.argv:
    print(os.path.abspath(os.curdir))
    print(os.listdir('.'))
    print(sys.path)

if os.path.abspath(os.curdir) in sys.path:
    from Difficult_Rocket import DR_runtime

    print(f'DR_version={DR_runtime.DR_version}')
    print(f'DR_language={DR_runtime.language}')
    # os.system(f'echo "DR_version={DR_runtime.DR_version}" >> $GITHUB_OUTPUT')

