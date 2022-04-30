/* by shenjackyuanjie  一些数据类型的转换 */

// 基本的头文件引用
#include<stdio.h>
#include<stdlib.h>


// 一些用于直观感受类型字节长度的数据类型
// 看着舒服而已（
// int 整数
#define int8 char
#define int16 short
#define int32 int
#define int64 long long
// uint 无符号整数
#define uint8 unsigned char
#define uint16 unsigned short
#define uint32 unsigned int
#define uint64 unsigned long long
// float 浮点数
#define float32 float
#define float64 double
// bool 布尔值
#define bool int8
#define true 1
#define false 0
// 字符串
#define string char*