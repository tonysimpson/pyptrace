#include <sys/ptrace.h>
#include <errno.h>

#include <Python.h>

static PyObject* _pyptrace(PyObject* self, PyObject *args)
{
    long request;
    long pid;
    long addr;
    long data;
    long ret;

    if (!PyArg_ParseTuple(args, "llll", &request, &pid, &addr, &data)) {
        return NULL;
    }

    ret = ptrace(request, pid, (void *) addr, (void *) data);
    return Py_BuildValue("l", ret);
}

static PyMethodDef pyptrace_funcs[] = {
    {
        "_pyptrace",
        (PyCFunction) _pyptrace,
        METH_VARARGS,
        "TODO"
    }, {
        NULL
    }
};

void init_pyptrace(void)
{
    Py_InitModule3("_pyptrace", pyptrace_funcs,
	    "C extension providing access to ptrace(2)");
}
