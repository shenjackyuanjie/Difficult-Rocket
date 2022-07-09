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

Py_UCS4 *get_ucs4from_unicode(PyObject *unicode){
    
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
            if (PyUnicode_Check(cache_obj) == 1) {  // 他不是个字符串(实际上如果有pyi文件就不需要这个检查)

            } else if (PyList_Check(cache_obj) == 1) {

            };
        };
        printf("text_len = %lld\n", (Py_size)text_len);

    };
    if(kwargs != NULL){ // 传入了 end 或者 sep
        Py_ssize_t kwargs_len = PyDict_Size(kwargs);
        printf("kwargs_len = %lld\n", (Py_size) kwargs_len);;
        if(PyDict_Contains(kwargs, PyUnicode_FromString("end"))){  // 如果包含 end 的参数
            PyObject *end_unicode; // 整个缓存
            end_unicode = PyDict_GetItemString(kwargs, "end");  // 先获取出来 Pyobj
            if(!PyUnicode_READY(end_unicode)){ return NULL; };  // 确认这个字符串对象可以用宏

            Py_ssize_t end_unicode_len = PyUnicode_GetLength(end_unicode);  // 缓存一手长度
            Py_UCS4 *new_end = malloc(sizeof(char) * end_unicode_len);  // 提前分配好不定长度的字符串内存
            for (Py_ssize_t i = 0; i < end_unicode_len; i++){
                new_end[i] = PyUnicode_ReadChar(end_unicode, i);  // 每一位对应读取
            };
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
}
