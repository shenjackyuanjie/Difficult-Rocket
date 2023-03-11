#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
from synology_api import filestation

# 输出 文档构建目录 的内容
docs_build = 'docs/book/html'

for root, dirs, files in os.walk(docs_build):
    print(root, dirs, files)

# 获取 token
token = os.environ['DSM_TOKEN']
username = os.environ['DSM_USERNAME']

fl = filestation.FileStation(ip_address='hws.shenjack.top',
                             port=5000,
                             username=username,
                             password=token,
                             secure=False,
                             cert_verify=False,
                             dsm_version=7,
                             debug=True)

print(fl.get_info())

print(fl.get_file_list('/web'))
