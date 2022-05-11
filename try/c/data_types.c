/*
-------------------------------
Difficult Rocket
Copyright © 2021-2022 by shenjackyuanjie
All rights reserved
-------------------------------
*/
// DR数据类型
// #include"Python.h"
#include<stdlib.h>
#include"data_utils.h" // 自己搓的一个常用数据类型的头文件

typedef struct ship_part // 一个部件的基本数据类型
{
    /* 一个 part 的数据格式 */
    string part_type;
    int32 part_id;
    float64 pois[6];
    /* 分别是： x, vx, y, vy, angle, vangle */
    bool flip_x;
    bool flip_y;
    bool part_enabled;
}ship_part;


int new_part(ship_part *pt){
    ship_part a_new_part;
    // pt -> a_new_part;
    return 0;
};


int main(){
    return 0;
}