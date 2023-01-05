import shutil


def copy():
    # 复制 ./docs/index.html 到 ../ 文件夹中
    try:
        shutil.copyfile('./docs/index.html', '../index.html')
    except OSError:
        pass

if __name__ == '__main__':
    copy()

