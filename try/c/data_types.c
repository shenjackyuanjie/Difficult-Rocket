#include<stdio.h>
#include<stdlib.h>
// DR data types

// 一些用于直观感受类型字节长度的数据类型
// 看着舒服而已（
#define int8 char
#define int16 short
#define int32 int
#define int64 long long
#define uint8 unsigned char
#define uint16 unsigned short
#define uint32 unsigned int
#define uint64 unsigned long long
#define float32 float
#define float64 double

struct part
{
    /* 一个 part 的数据格式 */
    long double a;
    uint16 b;
};

int main(){
    long double a = 1.0;
    // 输出 a 的字节长度
    printf("%o\n", sizeof(long double));
}

