#define PY_SSIZE_T_CLEAN
#include <stdio.h>
#include <stdlib.h>
#include <Python.h>

void print_it(wchar_t* out, wchar_t* end){
    printf("%s%s", out, end);
};

static PyObject *print_it_py(PyObject *self, PyObject *args){
    PyObject *back_obj = PyObject_Str(PyObject);
    return back_obj;
};