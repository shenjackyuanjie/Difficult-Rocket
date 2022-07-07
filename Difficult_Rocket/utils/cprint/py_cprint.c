//
// Created by shenjack on 2022/7/6.
//

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>

static PyObject *pycprint_print(PyObject *self, PyObject *args){
    const char *text;
    if(!PyArg_ParseTuple(args, "s", &text)){ // 解析 text
        return NULL;
    };
    printf("%s", text);
    Py_RETURN_NONE;
};

static PyObject *pycpint_printf(PyObject *self, PyObject *args, PyObject *kwargs){
    PyObject *a;
    if(!PyArg_ParseTuple(args, "O", &a)){
        return NULL;
    };

    Py_ssize_t text_len = PyTuple_Size(args);
    int int_text_len = (int)text_len;
    printf("%d", int_text_len);
    Py_RETURN_NONE;
};

static PyMethodDef PyCprintMethods[] = {
        {"print", pycprint_print, METH_VARARGS, "直接使用c的printf输出"},
        {"printf", (PyCFunction)(void(*))pycpint_printf, METH_VARARGS | METH_KEYWORDS,
         "传入类似py print然后进行format的print"},
        {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pycprintmodule = {
        PyModuleDef_HEAD_INIT,
        "pycprint",
        "直接调用c的printf",
        -1,
        PyCprintMethods
};

PyMODINIT_FUNC PyInit_pycprint(void){
    return PyModule_Create(&pycprintmodule);
}
