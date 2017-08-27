import os
import sys
import signal
import pyptrace

from pyptrace.ext import os as extos

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
 
    # run test
    print 'tracee: running execv()'
    ret = os.execv(tracee_path, [os.path.basename(tracee_path)])
 
    print 'failed execv:', ret
    sys.exit(ret)
 
elif pid > 0:  # within tracer
    print 'tracer: waiting for tracee to set traceme()'
    ret, status, errno = extos.waitpid(pid, 0)
    signo = extos.WSTOPSIG(status)
    print signo, extos.strsignal(signo)

    print 'tracer: setting tracee option PTRACE_O_EXITKILL'
    pyptrace.setoptions(pid, pyptrace.PTRACE_O_EXITKILL)

    # make execve of tracee happen
    print 'tracer: make tracee begin running execve'
    pyptrace.cont(pid)

    # wait for execve of tracee to stop
    print 'tracer: wait for execve of tracee to finish...'
    ret, status, errno = extos.waitpid(pid, 0)


    while True:
        bp_flag = pyptrace.DR7(0)
        pyptrace.pokeuser(pid, pyptrace.DR_OFFSET(0), 0x4005d6)
        pyptrace.pokeuser(pid, pyptrace.DR_OFFSET(7), bp_flag)

        pyptrace.cont(pid)
        ret, status, errno = extos.waitpid(pid, 0)

        if extos.WIFEXITED(status):
            print 'tracer, tracee exited'
            break

        signo = extos.WSTOPSIG(status)
        print 'tracer, stop signal: {}'.format(extos.strsignal(signo))
        ret, siginfo = pyptrace.getsiginfo(pid)
        if ret != 0:
            print 'tracer, failed to get tracee siginfo'
            continue

        if siginfo.si_signo != signal.SIGTRAP:
            continue

        if siginfo.si_code == pyptrace.SI_KERNEL:
            print 'sys trap'
        elif siginfo.si_code == extos.TRAP_TRACE:
            print 'process trap'
        elif siginfo.si_code == extos.TRAP_HWBKPT:
            print 'hardware break point'
        else:
            print 'unknown si_code: 0x%x' % siginfo.si_code

else:  # fork failed 
    # we don't care indeed, it's not gonna happen
    print 'fork failed'
    sys.exit()

