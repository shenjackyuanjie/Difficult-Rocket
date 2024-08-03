from cx_Freeze import setup, Executable
import tomli
import sys
sys.path.append(".")
from Difficult_Rocket import sdk_version

with open("pyproject.toml", "rb") as f:
    py_project = tomli.load(f)

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    "build_exe": "build/cx",
    "packages": [],
    "excludes": [
        "test",
        "asyncio",
        "tkinter",
        "unitest",
        "http",
        "html",
        "logging",
        "email",
        "distutils",
        "unittest",
        "concurrent",
        "pydoc_data",
        "lzma",
        "zipp",
        "nuitka",
        "PIL",
        "bz2",
        "numpy",
        "ssl"
    ],
    "zip_include_packages": ["pyglet"],
    "include_files": py_project["tool"]["lndl"]["nuitka"]["cli"]["include-data-dir"],
}

base = "console"

executables = [Executable("DR.py", base=base)]

setup(
    name="DR",
    version=str(sdk_version),
    description=py_project["tool"]["lndl"]["nuitka"]["cli"]["file-description"],
    options={"build_exe": build_options},
    executables=executables,
)
