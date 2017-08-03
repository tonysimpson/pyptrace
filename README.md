# pyptrace

pyptrace is a Python wrapper for Linux ptrace system call.

## Examples

This is an ecample of using pyptrace to trace execution of linux command `ls`:

```Python
  1 import os
  2 import sys
  3 import signal
  4 
  5 import pyptrace
  6 
  7 pid = os.fork()
  8 if pid == 0:  # child
  9     pyptrace.traceme()
 10     os.kill(os.getpid(), signal.SIGSTOP)
 11     ret = os.execv('/bin/ls', ['ls'])
 12     if ret:
 13         print 'failed running execv'
 14     sys.exit(ret)
 15 
 16 else:
 17     print 'pid:', pid
 18     ret = os.waitpid(pid, 0)
 19     print 'tracee stopped:', ret
 20     pyptrace.set_options(pid, pyptrace.PTRACE_O_EXITKILL)
 21 
 22     # now make execv happens
 23     print 'tracee continue, and exec begin'
 24     pyptrace.cont(pid)
 25 
 26     ret = os.waitpid(pid, 0)
 27     print 'exec finished:', ret
 28     # exec finished now
 29 
 30     def big_endian(int64num):
 31         intstr = '%016x' % (int64num % 0xffffffffffffffff)
 32         byte_arry = reversed([intstr[i:i+2] for i in xrange(0, len(intstr), 2)])
 33         return '0x' + ''.join(byte_arry)
 34     
 35     # binary data of program test should have been loaded into memory
 36     # let's check 
 37     step = 8
 38     main_start = 0x400659  # entry of main()
 39     for addr in xrange(main_start, main_start + step * 8, step):
 40         data = pyptrace.peektext(pid, addr)
 41         # print 'addr: %08x, %016x' % (addr, data & 0xffffffffffffffff)
 42         print 'addr: 0x%08x, %s' % (addr, big_endian(data))

```

## TODO

Not all ptrace requests are supported now, it's still under developement.

