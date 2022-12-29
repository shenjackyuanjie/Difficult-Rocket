#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys

from Difficult_Rocket import DR_runtime

print(os.curdir)
print(os.listdir('.'))
print(sys.path)

os.system(f'echo "DR_version={DR_runtime.DR_version.__str__()}" >> $GITHUB_OUTPUT')

