.. PyPtrace documentation master file, created by
   sphinx-quickstart on Sat Aug 19 18:18:32 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyPtrace
====================================

PyPtrace is a Python wrapper for `Linux ptrace system call <http://man7.org/linux/man-pages/man2/ptrace.2.html>`_.

1. Installation
----------------

.. code-block:: bash

    $ pip install pyptrace


2. Example Usage
-----------------

run_tracee.py is an example of using PyPtrace to tracee program execution, the code is as below

.. code-block:: python

    import os
    import sys
    import signal
    import pyptrace

    tracee_path = sys.argv[1]

    pid = os.fork()
    if pid == 0:  # within tracee
        # make this process tracable for tracer
        print 'tracee: run tracme()'
        pyptrace.traceme()
        print 'tracee: traceme() finished'

        print 'tracee: stop myself after running traceme()'
        os.kill(os.getpid(), signal.SIGSTOP)
        print 'tracee: tracee running again'
     
        # load tracee
        print 'tracee: running execv()'
        ret = os.execv(tracee_path, [os.path.basename(tracee_path)])
     
        print 'tracee: failed execv:', ret
        sys.exit(ret)
     
    elif pid > 0:  # within tracer
        print 'tracer: waiting for tracee to set traceme()'
        os.waitpid(pid, 0)

        print 'tracer: setting tracee option PTRACE_O_EXITKILL'
        pyptrace.setoptions(pid, pyptrace.PTRACE_O_EXITKILL)

        # make execve of tracee happen
        print 'tracer: make tracee begin running execve'
        pyptrace.cont(pid)

        # wait for execve of tracee to stop
        print 'tracer: wait for execve of tracee to finish...'
        os.waitpid(pid, 0)
        ret, regs = pyptrace.getregs(pid)
        print ret, regs
        print pyptrace.RegsWrapper(regs)

        regs.rip = 0x8848
        print 'setregs:', pyptrace.setregs(pid, regs)
        ret, regs = pyptrace.getregs(pid)
        print 'after'
        print pyptrace.RegsWrapper(regs)


        print 'tracer: execv of tracee finished, tracee stop again'
        print 'tracer: we can now set breakpoint to tracee'

    else:  # fork failed 
        # we don't care indeed, it's not gonna happen
        print 'fork failed'
        sys.exit()

Run run_tracee.py


.. code-block:: bash

    $ python run_tracee.py /bin/date
    tracer: waiting for tracee to set traceme()
    tracer: setting tracee option PTRACE_O_EXITKILL
    tracer: make tracee begin running execve
    tracer: wait for execve of tracee to finish...
    0 <pyptrace.X64UserRegs object at 0x7efe619aef80>
    {
        "gs": 0, 
        "gs_base": 0, 
        "rip": "0x00007f22dd69bc30", 
        "rdx": 0, 
        "r15": 0, 
        "cs": "0x0000000000000033", 
        "rax": 0, 
        "rsi": 0, 
        "rcx": 0, 
        "es": 0, 
        "r14": 0, 
        "fs": 0, 
        "r12": 0, 
        "r13": 0, 
        "r10": 0, 
        "r11": 0, 
        "orig_rax": "0x000000000000003b", 
        "fs_base": 0, 
        "rsp": "0x00007ffce5ff8680", 
        "ds": 0, 
        "rbx": 0, 
        "ss": "0x000000000000002b", 
        "r8": 0, 
        "r9": 0, 
        "rbp": 0, 
        "eflags": "0x0000000000000200", 
        "rdi": 0
    }
    setregs: 0
    after
    {
        "gs": 0, 
        "gs_base": 0, 
        "rip": "0x0000000000008848", 
        "rdx": 0, 
        "r15": 0, 
        "cs": "0x0000000000000033", 
        "rax": 0, 
        "rsi": 0, 
        "rcx": 0, 
        "es": 0, 
        "r14": 0, 
        "fs": 0, 
        "r12": 0, 
        "r13": 0, 
        "r10": 0, 
        "r11": 0, 
        "orig_rax": "0x000000000000003b", 
        "fs_base": 0, 
        "rsp": "0x00007ffce5ff8680", 
        "ds": 0, 
        "rbx": 0, 
        "ss": "0x000000000000002b", 
        "r8": 0, 
        "r9": 0, 
        "rbp": 0, 
        "eflags": "0x0000000000000200", 
        "rdi": 0
    }
    tracer: execv of tracee finished, tracee stop again
    tracer: we can now set breakpoint to tracee

3. References
-------------

3.1 pyptrace module
^^^^^^^^^^^^^^^^^^^

.. automodule:: pyptrace
   :members:

3.2 pyptrace.const module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: pyptrace.const
   :members:

