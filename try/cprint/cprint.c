//
// Created by shenjack on 2022/6/24.
//

//#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

// cPrint 主函数
static PyObject *PycPrint(PyObject *self, PyObject *args, PyObject *kwargs){
    // 解析参数
    const char *print_str;
    const char *line_end = NULL; // 准备参数
    static char *kwlist[] = {"some_stuf", "end", NULL}; // 准备参数列表
    if(!PyArg_ParseTupleAndKeywords(args, kwargs, "ss", kwlist, &print_str, &line_end)){
        return NULL;
    };
    if(line_end == NULL){
        line_end = "\n";
    };
    printf("%s%s", print_str, line_end);

    Py_RETURN_TRUE;
};

//static PyMethodDef cprintMethods[] = {
//        {"pyprint", (PyCFunction)(void(*)(void))PycPrint, METH_VARARGS | METH_KEYWORDS, },
//        {NULL, NULL, 0, NULL}
//};

int CcPrint(PyObject *self, PyObject *args, PyObject *kwargs){
    char *print_str;
    char *line_end = NULL; // 准备参数
    static char *kwlist[] = {"some_stuf", "end", NULL}; // 准备参数列表
    if(!PyArg_ParseTupleAndKeywords(args, kwargs, "ss", kwlist, &print_str, &line_end)){
        return 0;
    };
    return 1;
};

//static struct PyModuleDef cprintmodule = {
//        PyModuleDef_HEAD_INIT,
//        "cprint",
//        "直接使用c的printf",
//        -1,
//        cprintMethods
//};

//PyMODINIT_FUNC PyInit_cprint(void){
//    return PyModule_Create(&cprintmodule);
//}

// 如果你非得调用我·····
int main(){
    printf("aaaa");
    if(false){
        PycPrint(PyLong_FromLong(1), PyLong_FromLong(1), PyLong_FromLong(1));
    };
    return 0;
};