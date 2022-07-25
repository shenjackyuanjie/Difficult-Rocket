//
// Created by shenjack on 2022/7/6.
//

#define PY_SSIZE_T_CLEAN
#define Py_size long long int
#include <Python.h>
#include <stdint.h>



int *print_PyUcs4(PyObject *pyObject){
    if(PyUnicode_READY(pyObject) == -1){
        PyErr_SetString(PyExc_UnicodeDecodeError, "failed");
        return NULL;
    }
    #if defined(__linux__)
    const char *out_char = PyUnicode_AsUTF8(pyObject);
    printf("%s", out_char);
    #elif defined(WIN32) || defined(_WIN32) || defined(__WIN32__) || defined(__NT__)
    Py_UCS4 *ucs4 = PyUnicode_4BYTE_DATA(pyObject);
    printf("%ws", ucs4); // win
    #endif
    return (int *) 1;
};

static PyObject *pycprint_print(PyObject *self, PyObject *args){
    if(!print_PyUcs4(PyTuple_GetItem(args, 0))){
        return NULL;
    };
    Py_RETURN_NONE;
};

const char *get_char_from_PyUnicode(PyObject *unicodeObject){
    if(!PyUnicode_READY(unicodeObject)){
        return NULL;
    };
    const char *char_obj = PyUnicode_AsUTF8(unicodeObject);
    if(char_obj == NULL){
        return NULL;
    } else {
        return char_obj;
    };
};


static PyObject *pycpint_printf(PyObject *self, PyObject *args, PyObject *kwargs){
    printf("args == NULL: %d\n", args == NULL);
    printf("kwargs == NULL: %d\n", kwargs == NULL);

    const char *end = "\n";
    const char *sep = " ";

    if (args != NULL){ // 传入了字符串
        Py_ssize_t text_len = PyTuple_Size(args); // 获取字符串的长度
        PyObject *cache_obj; // 创建一个缓存

        for (Py_ssize_t i = 0; i < text_len; i++){  // for 遍历
            cache_obj = PyTuple_GetItem(args, i);  // 获取一个字符串
            if (cache_obj == NULL){ return NULL; };  // 出毛病了就报错

            if (PyUnicode_Check(cache_obj) == 1) {
                print_PyUcs4(cache_obj);
            } else if (PyList_Check(cache_obj) == 1) {

            };
        };
        printf("text_len = %lld\n", (Py_size)text_len);
    };
    if(kwargs != NULL){ // 传入了 end 或者 sep
        Py_ssize_t kwargs_len = PyDict_Size(kwargs);
        printf("kwargs_len = %lld\n", (Py_size) kwargs_len);;
        if(PyDict_Contains(kwargs, PyUnicode_FromString("end"))){ // 如果包含 end 的参数

            PyObject *end_unicode = PyDict_GetItemString(kwargs, "end");  // 先获取出来 Pyobj

            end = PyUnicode_AsUTF8(end_unicode);
        };
    };
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
};
