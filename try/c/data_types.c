// DR数据类型
#include <stdlib.h>
#include "data_utils.h" // 自己搓的一个常用数据类型的头文件

struct ship_part
{
    /* 一个 part 的数据格式 */
    string part_type;
    int32 part_id;
    bool enabled;
    float64 x;
    float64 v_x;
    float64 y;
    float64 v_y;
    float32 angle;
    float64 v_angle;
    bool flip_x;
    bool flip_y;
} ship_part = {
    "pod",
    0,
    false,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    false,
    false
};

int main(){
    // 创建一个 part
    struct ship_part p;
    p.part_type = "head";
    p.part_id = 1;
    p.enabled = true;

    // 创建一个 part 的数组
    struct ship_part *parts = malloc(sizeof(struct ship_part) * 10);

    // 输出一个 part 的数据
    printf("%s %d %d %f %f %f %f %f %f %d %d\n",
        p.part_type, p.part_id, p.enabled,
        p.x, p.v_x, p.y, p.v_y, p.angle, p.v_angle,
        p.flip_x, p.flip_y);

    return 0;
}
