import _pyptrace
from const import *


def attach(pid):
    return _pyptrace._pyptrace(PTRACE_ATTACH, pid, 0, 0)

def cont(pid, signo=0):
    return _pyptrace._pyptrace(PTRACE_CONT, pid, 0, signo)

def traceme():
    return _pyptrace._pyptrace(PTRACE_TRACEME, 0, 0, 0)

def detach(pid, signo):
    return _pyptrace._pyptrace(PTRACE_DETACH, pid, 0, signo)
