#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys


print(os.path.abspath(os.curdir))
print(os.listdir('.'))
sys.path.append(os.path.abspath(os.curdir))
print(sys.path)

from Difficult_Rocket import DR_runtime

print(f'DR_version={DR_runtime.DR_version}')
os.system(f'echo "DR_version={DR_runtime.DR_version}" >> $GITHUB_OUTPUT')

