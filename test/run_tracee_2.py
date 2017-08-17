import os
import sys
import signal
import pyptrace

pid = os.fork()
if pid == 0:  # within tracee
    # make this process tracable for tracer
    print 'tracee: run tracme()'
    pyptrace.traceme()
    print 'tracee: traceme() finished'

    print 'tracee: stop myself after running traceme()'
    os.kill(os.getpid(), signal.SIGSTOP)
    print 'tracee: tracee running again'
 
    # run test
    print 'tracee: running execv()'
    ret = os.execv('./test', ['test'])
 
    print 'failed execv:', ret
    sys.exit(ret)
 
elif pid > 0:  # within tracer
    print 'tracer: waiting for tracee to set traceme()'
    os.waitpid(pid, 0)

    print 'tracer: setting tracee option PTRACE_O_EXITKILL'
    pyptrace.set_options(pid, pyptrace.PTRACE_O_EXITKILL)

    print 'tracer: begin tracing tracee...'
else:  # fork failed 
    # we don't care indeed, it's not gonna happen
    print 'fork failed'
    sys.exit()

