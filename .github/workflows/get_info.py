#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys
import rtoml

sys.path.append(os.path.abspath(os.curdir))

from Difficult_Rocket import DR_runtime

args = ['-env', '-github-dev']

if sys.argv == '':  # 没有输入参数，直接输出默认信息并输出
    print(sys.version)
    from Difficult_Rocket.utils import tools
    # 重置窗口信息
    config_file = tools.load_file('./configs/main.toml')
    config_file['window']['width'] = 1024
    config_file['window']['height'] = 768
    rtoml.dump(config_file, open('./configs/main.toml', 'w'))

elif os.path.abspath(os.curdir) in sys.path and sys.argv == '-env':
    with open('./.github/workflows/env.ps1', encoding='utf-8', mode='w') as env_file:
        print(f'$env:DR_version = "{DR_runtime.DR_version}"', file=env_file)
        print(f'$env:DR_language = "{DR_runtime.language}"', file=env_file)
        print(f'$env:DR_long_version = "{DR_runtime.DR_long_version}"', file=env_file)
        print(f'$env:Build_version = "{DR_runtime.Build_version}"', file=env_file)

elif os.path.abspath(os.curdir) in sys.path and sys.argv == '-github-env':

    print(f'DR_version={DR_runtime.DR_version}')
    print(f'DR_language={DR_runtime.language}')
    print(f'DR_long_version={DR_runtime.DR_long_version}')
    print(f'Build_version={DR_runtime.Build_version}')
