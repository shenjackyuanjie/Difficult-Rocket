import sys
import shutil

from pathlib import Path

"""
将 DR_game 复制到指定位置 (默认为 ./build/dr_game)

也许以后会支持自动复制别的模组
"""


def pack_mod_to(dest: Path):
    src = Path("./mods/dr_game")
    if not src.exists():
        print(f"未找到 {src}")
        sys.exit(1)

    if not dest.exists():
        dest.mkdir(parents=True, exist_ok=True)
    else:
        if not dest.is_dir():
            print(f"{dest} 不是文件夹！")
            return
        if dest.exists():
            shutil.rmtree(dest)
            dest.mkdir(parents=True, exist_ok=True)

    # 先遍历所有根目录下的.py文件
    for file in src.glob("*.py"):
        # 复制到目标目录
        dest_file = dest / file.name
        print(f"复制 {file} -> {dest_file}")
        shutil.copy2(file, dest_file)

    # 复制 lang 文件夹
    lang_src = src / "lang"
    lang_dest = dest / "lang"
    if lang_src.exists():
        print(f"复制 {lang_src} -> {lang_dest}")
        shutil.copytree(lang_src, lang_dest)

    # 处理 "Difficult_Rocket_rs" 文件夹
    if (src / "Difficult_Rocket_rs").exists():
        print("处理 Difficult_Rocket_rs 文件夹...")

        dr_rs_src = src / "Difficult_Rocket_rs"
        dr_rs_dest = dest / "Difficult_Rocket_rs"
        dr_rs_dest.mkdir(parents=True, exist_ok=True)

        # 复制 __init__.py
        shutil.copy2(dr_rs_src / "__init__.py", dr_rs_dest)

        (dr_rs_dest / "lib").mkdir(parents=True, exist_ok=True)
        # 复制 lib 文件夹下的 __init__.py
        shutil.copy2(dr_rs_src / "lib" / "__init__.py", dr_rs_dest / "lib")

        # 复制 lib 文件夹下的 so/pyd 文件
        for file in dr_rs_src.glob("lib/*.so"):
            dest_file = dr_rs_dest / "lib" / file.name
            print(f"复制 so {file} -> {dest_file}")
            shutil.copy2(file, dest_file)
        for file in dr_rs_src.glob("lib/*.pyd"):
            dest_file = dr_rs_dest / "lib" / file.name
            print(f"复制 pyd {file} -> {dest_file}")
            shutil.copy2(file, dest_file)

    print("复制完成！")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("将会把 dr game 复制到 ./build/dr_game")
        if input("是否继续？(y/n)").lower() != "y":
            sys.exit(0)
        pack_mod_to(Path("./build") / "dr_game")

    elif sys.argv[1] == "-y":
        # 如果是 -y 参数，直接复制到默认位置
        pack_mod_to(Path("./build") / "dr_game")

    elif sys.argv[1] == "-h":
        # 如果是 -h 参数，打印帮助信息
        print("Usage: pack_dr_mod.py [dest]")
        print("dest: 复制到的目标目录")
        print("如果未指定目标目录，则默认为 ./build/dr_game")
        sys.exit(0)

    else:
        # 否则复制到指定位置
        pack_mod_to(Path(sys.argv[1]))
