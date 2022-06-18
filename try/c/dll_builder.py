#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

import os
import sys
import getopt

# input_args = sys.argv

# print(input_args)
filename = "./data_types.c"
dllname = "./data_types.dll"

python_include_path = "C:/Users/shenjack.SHENJACK-5600X/AppData/Local/Programs/Python/Python38/include/"

os.system("gcc -O3 -I {} -shared {} -o {}".format(python_include_path, filename, dllname))
# gcc -I C:/Users/shenjack.SHENJACK-5600X/AppData/Local/Programs/Python/Python38/include/ -shared .\data_types.c -o .\data_types.dll
