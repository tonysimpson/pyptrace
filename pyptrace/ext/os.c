#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>

#include <Python.h>

static PyObject* _waitpid(PyObject* self, PyObject* args)
{
    long pid;
    int status, options, ret;

    if (!PyArg_ParseTuple(args, "li", &pid, &options)) {
        return NULL;
    }


    ret = waitpid(pid, &status, options);
    return Py_BuildValue("(ii)", ret, status);
}

static PyMethodDef os_funcs[] = {
    {
        "waitpid",
        (PyCFunction) _waitpid,
        METH_VARARGS,
        "TODO"
    }, {
        NULL
    }
};

void initos(void)
{
    Py_InitModule3("os", os_funcs,
        "Wrapper for some usefull os calls.");
}
