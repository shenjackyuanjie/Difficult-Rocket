#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import random
import unittest

from libs.pyglet_rs import Vector2_rs, Vector3_rs, Vector4_rs


# 用于自动在测试运行前后输出测试信息的装饰器
def print_test_info(func):
    def wrapper(*args, **kwargs):
        print(f"{'=' * 20} {func.__name__} {'=' * 20}")
        func(*args, **kwargs)
        print(f"{'=' * 20} {func.__name__} {'=' * 20}")

    return wrapper


class TestVector(unittest.TestCase):
    @print_test_info
    def test1_create_print_vector(self):
        vec2 = Vector2_rs(1, 2)
        vec3 = Vector3_rs(1, 2, 3)
        vec4 = Vector4_rs(1, 2, 3, 4)

        print(f"{vec2=}")
        print(f"{vec3=}")
        print(f"{vec4=}")

    @print_test_info
    def test2_calculate_vector(self):
        vec2 = Vector2_rs(random.randint(1, 100), random.randint(1, 100))
        vec3 = Vector3_rs(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100))
        vec4 = Vector4_rs(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100), random.randint(1, 100))

        vec2_1 = Vector2_rs(random.randint(1, 100), random.randint(1, 100))
        vec3_1 = Vector3_rs(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100))
        vec4_1 = Vector4_rs(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100), random.randint(1, 100))

        print(f"{vec2=} {vec2_1=}")
        print(f"{vec3=} {vec3_1=}")
        print(f"{vec4=} {vec4_1=}")

        print(f"{vec2 + vec2_1=}")
        print(f"{vec3 + vec3_1=}")
        print(f"{vec4 + vec4_1=}")

        print(f"{vec2 - vec2_1=}")
        print(f"{vec3 - vec3_1=}")
        print(f"{vec4 - vec4_1=}")

        print(f"{vec2 * vec2_1=}")
        print(f"{vec3 * vec3_1=}")
        print(f"{vec4 * vec4_1=}")

        print(f"{vec2 / vec2_1=}")
        print(f"{vec3 / vec3_1=}")
        print(f"{vec4 / vec4_1=}")

        print(f"{vec2 // vec2_1=}")
        print(f"{vec3 // vec3_1=}")
        print(f"{vec4 // vec4_1=}")