#include <python2.7/Python.h>
#include "analyze.h"

static const char *GEOPHONE_NAME = "Geophone";

static PyObject * wrapper(PyObject *self, PyObject *args) {
    const int * array;
    int n;
    if (!PyArg_ParseTuple(args, "s", &array)) {//这句是把python的变量args转换成c的变量command
      return NULL;
    }
    n = analyze(array);//调用c的函数
    return Py_BuildValue("i", n);//把c的返回值n转换成python的对象
}

static PyMethodDef sGeophoneMethods[] = {
    { "analyze", wrapper, METH_VARARGS, "Pass a list to analyze data." },
    { NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC initGeophone() {
    PyObject *m = Py_InitModule(GEOPHONE_NAME, sGeophoneMethods);
    if (m == NULL) {
        return;
    }
}
