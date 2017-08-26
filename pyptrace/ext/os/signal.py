import ctypes

class _fKill(ctypes.Structure):
    _fields_ = [
        ('si_pid', ctypes.c_long),
        ('si_uid', ctypes.c_long)
    ]

class Sifields(ctypes.Union):
    _fields_ = [
        ('_pad', ctypes.c_int * (128 / 4 - 4)),
        ('_kill', _fKill),
    ]

class Siginfo(ctypes.Structure):
    _fields_ = [
        ('si_signo',    ctypes.c_int),
        ('si_errno',    ctypes.c_int),
        ('si_code',     ctypes.c_int)
    ]

_libc = ctypes.cdll.LoadLibrary('libc.so.6')
def strsignal(signo):
    _libc_strsignal = _libc.strsignal
    _libc_strsignal.restype = ctypes.c_char_p
    _libc_strsignal.argtypes = (ctypes.c_int,)

    ret = _libc_strsignal(signo)
    return ret
