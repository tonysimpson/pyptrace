#include <Python.h>
#include <sys/ptrace.h>

static PyObject* traceme(PyObject* self)
{
    long ret;

    ret = ptrace(PTRACE_TRACEME, 0, NULL, NULL);
    return Py_BuildValue("l", ret);
}

static PyObject* attach(PyObject *self, PyObject *args)
{
    long ret;
    long pid;

    if (!PyArg_ParseTuple(args, "l", &pid)) {
	return NULL;
    }

    ret = ptrace(PTRACE_ATTACH, pid, NULL, NULL);
    return Py_BuildValue("l", ret);
}

static PyObject* cont(PyObject *self, PyObject *args)
{
    long ret;
    long pid;

    if (!PyArg_ParseTuple(args, "l", &pid)) {
	return NULL;
    }

    ret = ptrace(PTRACE_CONT, pid, NULL, NULL);
    return Py_BuildValue("l", ret);
}

static PyObject* setoptions(PyObject *self, PyObject *args)
{
    long ret;
    long pid;
    long options;

    if (!PyArg_ParseTuple(args, "ll", &pid, &options)) {
	return NULL;
    }

    ret = ptrace(PTRACE_SETOPTIONS, pid, NULL, (void *) options);
    return Py_BuildValue("l", ret);
}

static PyMethodDef pyptrace_funcs[] = {
    {
	"traceme",
	(PyCFunction) traceme, 
	METH_NOARGS,
    	"Indicate that this process is to be traced by its parent.\n"
    }, {
	"attach",
	(PyCFunction) attach,
	METH_VARARGS,
	"Attach  to  the process specified in pid, making it a tracee of the calling process.\n"
    }, {
	"cont",
	(PyCFunction) cont,
	METH_VARARGS,
	"Restart  the  stopped  tracee  process.\n"
    }, {
	"setoptions",
	(PyCFunction) setoptions,
	METH_VARARGS,
	"Set  ptrace  options from data.\n"

    }, {
	NULL
    }
};

void initpyptrace(void)
{
    Py_InitModule3("pyptrace", pyptrace_funcs,
	    "C extension providing access to ptrace(2)");
}
