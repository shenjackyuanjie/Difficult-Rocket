
#include"utils.h"

struct part
{
    /* 一个 part 的数据格式 */
    long double a;
    uint16 b;
};

int main(){
    long double a = 1.0;
    // 输出 a 的字节长度
    printf("%d\n", sizeof(long double));
}

