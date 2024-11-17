import argparse

"""
#   DR basic running from source
#   DR build (by nuitka)
#   DR contributing
"""

# fmt: off
basic = {
    "images": [
        'pillow >= 10.4.0; (platform_python_implementation == "PyPy" and '
        'python_version < "3.13" and python_version > "3.8") or '
        'platform_python_implementation == "CPython"',
    ],
    "sys info": [
        "psutil >= 6.0.0"
    ],
    "file read": [
        "tomli >= 2.0.2",
        "tomli-w >= 1.0.0",
        "defusedxml >= 0.7.1"
    ],
}

build = {
    "compile": [
        "nuitka >= 2.4",
        "imageio >= 2.34.2",
        "setuptools >= 69",
        "setuptools-rust >= 1.10.2",
        "wheel >= 0.43.0",
    ]
}

dev = {
    "debug": [
        "objprint >= 0.2.3",
        "viztracer >= 0.16.3; platform_python_implementation != \"PyPy\"",
        "vizplugins >= 0.1.3; platform_python_implementation != \"PyPy\""
    ]
}
# fmt: on

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "type", help="type of genrating require", default=0, type=int, choices=[0, 1, 2]
    )
    args = parser.parse_args()

    out = []
    if args.type >= 0:
        out.append("# DR basic running from source\n\n")
        for tag, package in basic.items():
            out.append(f"# for {tag}\n")
            for p in package:
                out.append(f"{p}\n")
        out.append("\n")
    if args.type >= 1:
        out.append("# DR build (by nuitka)\n\n")
        for tag, package in build.items():
            out.append(f"# for {tag}\n")
            for p in package:
                out.append(f"{p}\n")
        out.append("\n")
    if args.type >= 2:
        out.append("# DR contributing\n\n")
        for tag, package in dev.items():
            out.append(f"# for {tag}\n")
            for p in package:
                out.append(f"{p}\n")
    print("".join(out))

    with open("requirements.txt", "w") as f:
        f.writelines(out)
