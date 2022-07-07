//
// Created by shenjack on 2022/6/24.
//

//#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>


int CcPrint(PyObject *self, PyObject *args, PyObject *kwargs){
    char *print_str;
    char *line_end = NULL; // 准备参数
    static char *kwlist[] = {"some_stuf", "end", NULL}; // 准备参数列表
    if(!PyArg_ParseTupleAndKeywords(args, kwargs, "ss", kwlist, &print_str, &line_end)){
        return 0;
    };
    return 1;
};

// 如果你非得调用我·····
int main(){
    printf("aaaa");
    if(false){
        CcPrint(PyLong_FromLong(1), PyLong_FromLong(1), PyLong_FromLong(1));
    };
    return 0;
};