#include <python2.7/Python.h>
#include "analyze.h"
static const char *GEOPHONE_NAME = "FFT";

static PyObject * wrapper(PyObject *self, PyObject *args) {
    //
    PyObject *i_arr, *item;
    long power;
    int fft_data[FFTSIZE+1], i;
    if(!PyArg_ParseTuple(args, "O", &i_arr) ){//O for PyObject
        return NULL;
    }
    if(!PySequence_Check(i_arr)){
        PyErr_SetString(PyExc_TypeError, "expected sequence");
        return NULL;
    }
    for(i=0; i<FFTSIZE; i++){
        item = PySequence_GetItem(i_arr, i);//把数据依次取出来
        if(!PyInt_Check(item)){
            PyErr_SetString(PyExc_TypeError, "expected sequence of integers");
            return NULL;
        }
        fft_data[i] = PyInt_AsLong(item);//把数据转成c的int并放入数组中
        Py_DECREF(item);                //取消一个引用计数s
    }
    power = getFFTPower(fft_data);//调用c的函数
    return Py_BuildValue("l", power);//把c的返回值power转换成python的整型对象*/
}

static PyMethodDef GeophoneMethods[] = {
    {"getFFTPower", wrapper, METH_VARARGS, "Pass a list to analyze."},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC initFFT() {
    PyObject *m = Py_InitModule(GEOPHONE_NAME, GeophoneMethods);
    if (m == NULL) {
        return;
    }
}
