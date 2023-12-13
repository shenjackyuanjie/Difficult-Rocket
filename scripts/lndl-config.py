#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import platform

from Difficult_Rocket import sdk_version, build_version

from lib_not_dr.nuitka import nuitka_config_type, raw_config_type


def gen_pyglet_no_follow_import() -> list:
    no_follow_import = []
    no_follow_import += [f"pyglet.app.{x}" for x in ["win32", "xlib", "cocoa"]]
    no_follow_import += [f"pyglet.input.{x}" for x in ["win32", "linux", "macos"]]
    no_follow_import += [
        f"pyglet.libs.{x}"
        for x in ["win32", "x11", "wayland", "darwin", "egl", "headless"]
    ]
    no_follow_import += [
        f"pyglet.window.{x}" for x in ["win32", "xlib", "cocoa", "headless"]
    ]
    no_follow_import += [
        f"pyglet.canvas.{x}"
        for x in (
            "win32",
            "xlib",
            "xlib_vidmoderstore",
            "cocoa",
            "headless",
        )
    ]
    no_follow_import += [f"pyglet.gl.{x}" for x in ["win32", "xlib", "cocoa", "headless"]]

    mult_plat_libs = ["app", "input", "libs", "window", "canvas", "gl"]
    if platform.system() == "Windows":
        for lib in mult_plat_libs:
            no_follow_import.remove(f"pyglet.{lib}.win32")
    elif platform.system() == "Linux":
        for lib in mult_plat_libs:
            for name in ("xlib", "x11", "wayland", "egl"):
                if f"pyglet.{lib}.{name}" in no_follow_import:
                    no_follow_import.remove(f"pyglet.{lib}.{name}")
        no_follow_import.remove("pyglet.canvas.xlib_vidmoderstore")
    elif platform.system() == "Darwin":
        for lib in mult_plat_libs:
            for name in ("cocoa", "darwin", "macos"):
                if f"pyglet.{lib}.{name}" in no_follow_import:
                    no_follow_import.remove(f"pyglet.{lib}.{name}")
    return no_follow_import


def main(config: raw_config_type) -> nuitka_config_type:
    print("debug", config)
    config = config["cli"]
    if platform.system() == "Darwin":
        config.pop("windows-icon-from-ico")
        config.pop("linux-icon")
    elif platform.system() == "Linux":
        config.pop("windows-icon-from-ico")
        config.pop("macos-app-icon")
    elif platform.system() == "Windows":
        config.pop("linux-icon")
        config.pop("macos-app-icon")

    config["file-version"] = str(build_version)
    config["product-version"] = str(sdk_version)
    config["macos-app-version"] = str(sdk_version)

    config["nofollow-import-to"] += gen_pyglet_no_follow_import()
    config["output-dir"] = "./build/nuitka-" + platform.system().lower()

    print("done", config)
    return config
