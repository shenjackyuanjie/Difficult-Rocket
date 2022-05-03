/*
-------------------------------
Difficult Rocket
Copyright © 2021-2022 by shenjackyuanjie
All rights reserved
-------------------------------
*/
// DR数据类型
#include"Python.h"
#include<stdlib.h>
#include"data_utils.h" // 自己搓的一个常用数据类型的头文件

struct ship_part // 一个部件的基本数据类型
{
    /* 一个 part 的数据格式 */
    string part_type;
    int32 part_id;
    float64 x;
    float64 v_x;
    float64 y;
    float64 v_y;
    float64 angle;
    float64 v_angle;
    // TODO 会改成基于 float 64的数组
    bool flip_x;
    bool flip_y;
    bool part_enabled;
    // TODO 也改成数组
} a_ship_part = {
    "pod",
    0,
    0, 0, 0, 0, 0, 0,
    false, false, false
};

struct ship_part a_part;
// a_part = {};

int main(){
    return 0;
}