#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys
import rtoml

sys.path.append(os.path.abspath(os.curdir))
if '-env' not in sys.argv:
    print(sys.version)
    print(os.getenv('env:GITHUB_SHA'))
    from Difficult_Rocket.utils import tools
    # 重置窗口信息
    config_file = tools.load_file('./configs/main.toml')
    config_file['window']['width'] = 1024
    config_file['window']['height'] = 768
    rtoml.dump(config_file, open('./configs/main.toml', 'w'))

if os.path.abspath(os.curdir) in sys.path:
    from Difficult_Rocket import DR_runtime

    print(f'DR_version={DR_runtime.DR_version}')
    print(f'DR_language={DR_runtime.language}')
    print(f'DR_long_version={DR_runtime.DR_long_version}')
    # os.system(f'echo "DR_version={DR_runtime.DR_version}" >> $GITHUB_OUTPUT')

