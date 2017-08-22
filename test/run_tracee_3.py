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

