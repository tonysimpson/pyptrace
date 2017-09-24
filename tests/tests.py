import time
import traceback
import unittest
import subprocess
from contextlib import contextmanager
import pyptrace

LOOP_FOREVER = './loop_forever'

@contextmanager
def create_process_ctx(ppath):
    proc = subprocess.Popen(ppath)

    try:
        yield proc
    except Exception, e:
        raise e
    finally:  # clean up
        retcode = proc.poll() 
        if retcode is None:
            proc.terminate()

class PyPtraceTest(unittest.TestCase):
    def test_attach_and_detach(self):
        with create_process_ctx(LOOP_FOREVER) as proc:
            pid = proc.pid
            ret = pyptrace.attach(pid)
            if ret != 0:
                self.fail('attach failed!')

            ret, _, _ = pyptrace.extos.waitpid(pid, 0)
            if ret != pid:
                self.fail('attach failed!')

            ret = pyptrace.detach(pid, 0)
            if ret != 0:
                self.fail('detach failed!')

            time.sleep(1)

if __name__ == '__main__':
    unittest.main()
