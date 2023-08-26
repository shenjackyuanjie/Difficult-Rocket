#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import time
from pprint import pprint
from synology_api import filestation


class DSM:
    def __init__(self, docs_path: str, dsm_path: str):
        self.docs_path = docs_path
        self.dsm_path = dsm_path
        self.token = os.environ['DSM_TOKEN']
        self.fl = filestation.FileStation(ip_address='hws.shenjack.top',
                                          port=5000,
                                          username='github',
                                          password=self.token,
                                          secure=False,
                                          cert_verify=False,
                                          dsm_version=7,
                                          debug=True,
                                          interactive_output=False)

    def list_files(self):
        # 输出 文档构建目录 的内容
        print(f'==========输出 {self.docs_path} 的内容==========')
        for root, dirs, files in os.walk(self.docs_path):
            print(root, dirs)
        print('==========就这些==========')

    def clear_dsm(self):
        # 清空 DSM 的 /web/dr 目录
        delete_task = self.fl.start_delete_task(self.dsm_path, recursive=True)
        delete_task_id = delete_task['taskid']
        time.sleep(1)  # 等待 1 秒 保证任务已经完成
        pprint(self.fl.get_delete_status(delete_task_id)['data']['finished'])

    def check_md5(self, local_md5: str) -> bool:
        """
        检查本地构建的文档和 DSM 上的文档的 md5 是否一致
        :param local_md5:
        :return: True: 一致 False: 不一致
        """
        # 打开提供的md5文件
        try:
            with open(local_md5, 'r', encoding='utf-8') as f:
                md5 = f.read()
        except FileNotFoundError:
            print(f'文件 {local_md5} 不存在')
            return False
        # 检测是否存在 dsm 上的 md5.txt
        dsm_files = self.fl.get_file_list(folder_path='/web/dr')
        if dsm_files.get('error'):
            print(dsm_files['error'])
            return False
        dsm_files = dsm_files['data']['files']
        if '/web/dr/md5.txt' not in [file['path'] for file in dsm_files]:
            print('dsm md5.txt 不存在')
            return False
        # 下载 dsm 上的 md5.txt
        try:
            self.fl.get_file(path='/web/dr/md5.txt', mode='download', dest_path='./docs/book')
            with open('./docs/book/md5.txt', 'r', encoding='utf-8') as f:
                md5_last = f.read()
            if md5 == md5_last:
                return True
        except Exception as e:
            print(e)
            return False

    def upload_docs(self, local_md5: str):
        # 上传本地构建的文档到 DSM
        print(f'==========上传 {self.docs_path} 到 {self.dsm_path}==========')
        # 使用 os.walk 递归遍历文件夹 依次按照对应路径上传
        # 上传的时候 目标路径为本地路径的相对路径
        for root, dirs, files in os.walk(self.docs_path):
            for file in files:
                file_path = os.path.join(root, file)
                dest_path = f'{self.dsm_path}{root[len(self.docs_path):]}'
                dest_path = dest_path.replace('\\', '/')
                # 输出 文件路径 和 目标路径
                print(f'{file_path} -> {dest_path}', end=' ')
                pprint(self.fl.upload_file(dest_path=dest_path,
                                           file_path=file_path,
                                           overwrite=True))
                # self.fl.upload_file(dest_path=dest_path,
                #                     file_path=file_path,
                #                     overwrite=True)
        # 上传本地的 md5 文件
        print(f'{local_md5} -> {self.dsm_path}', end=' ')
        pprint(self.fl.upload_file(dest_path=self.dsm_path,
                                   file_path=local_md5,
                                   overwrite=True))
        print('==========上传完成==========')


def main():
    docs_path = 'docs/book'
    dsm_path = '/web/dr'
    dsm = DSM(docs_path, dsm_path)
    dsm.list_files()
    if dsm.check_md5('docs/md5.txt'):
        print('md5 一致，不需要上传')
        return 0
    dsm.clear_dsm()
    dsm.upload_docs('docs/md5.txt')

    dsm.fl.logout()


if __name__ == '__main__':
    main()
