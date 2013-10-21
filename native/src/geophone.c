#include <python2.7/Python.h>
#include "analyze.h"
static const char *GEOPHONE_NAME = "FFT";

static PyObject * wrapper(PyObject *self, PyObject *args) {
    //
    PyObject *i_arr, *item;
    long power;
    int fft_data[FFTSIZE+1], i;
    if(!PyArg_ParseTuple(args, "O", &i_arr) ){//i for int, O for PyObject
        return NULL;
    }
    if(!PySequence_Check(i_arr)){
        PyErr_SetString(PyExc_TypeError, "expected sequence");
        return NULL;
    }
    for(i=0; i<FFTSIZE; i++){
        item = PySequence_GetItem(i_arr, i);
        if(!PyInt_Check(item)){
            PyErr_SetString(PyExc_TypeError, "expected sequence of integers");
            return NULL;
        }
        fft_data[i] = PyInt_AsLong(item);
        Py_DECREF(item);
    }
    power = getFFTPower(fft_data);//调用c的函数
    return Py_BuildValue("l", power);//把c的返回值n转换成python的对象*/
    
    /*
     const int *array;
     long n;
     if (!PyArg_ParseTuple(args, "o!", &PyList_Type, &array)) {//这句是把python的变量args转换成c的变量
     return NULL;
     }
     
     n = getFFTPower(array);//调用c的函数
     return Py_BuildValue("l", n);//把c的返回值n转换成python的对象*/
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
