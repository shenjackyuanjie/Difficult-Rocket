#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

import ctypes

ctypes.cdll.LoadLibrary('./data_types.dll')

data_type_dll = ctypes.CDLL("./data_types.dll")

print(data_type_dll)

a = data_type_dll.a_part

print(a)

print(a.part_type)
