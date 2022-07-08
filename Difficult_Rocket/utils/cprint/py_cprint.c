//
// Created by shenjack on 2022/7/6.
//

#define PY_SSIZE_T_CLEAN
#define Py_size long long int
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
    printf("args == NULL: %d\n", args == NULL);
    printf("kwargs == NULL: %d\n", kwargs == NULL);

    const char *end = "\n";
    const char *sep = " ";

    if(args != NULL){ // 传入了字符串
        Py_ssize_t text_len = PyTuple_Size(args);


        printf("text_len = %lld\n", (Py_size)text_len);
        char *text_list;
        char **text_lists = malloc(sizeof(char) * text_len);
        const char *args_text = malloc(sizeof(char) * text_len);

        PyArg_ParseTuple(args, , &);
    };
    if(kwargs != NULL){ // 传入了 end 或者 sep
        Py_ssize_t kwargs_len = PyDict_Size(kwargs);
        printf("kwargs_len = %lld\n", (Py_size) kwargs_len);;
        char *kwlist[] = {"end", "sep", NULL};
        PyArg_ParseTupleAndKeywords(args, kwargs, "ss", kwlist, &end, &sep);
    };
    Py_ssize_t text_len = PyTuple_Size(args);
    printf("%s", end);
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
