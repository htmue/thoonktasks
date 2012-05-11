# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2012-02-29.
#=============================================================================
#   worker.py --- Task queue worker
#=============================================================================
from thoonktasks import _queues, BaseObject


class Worker(BaseObject):

    def __init__(self, queue='default'):
        self._queue = queue
        self._jobs = self._thoonk.job(self._queue)
        
    def work_once(self, timeout=0):
        job, request, _ = self._jobs.get(timeout)
        self._do_job(job, request)

    def _do_job(self, job, request):
        name, args, kwargs = self.deserialize(request)
        task = _queues[self._queue][name]
        try:
            result = task._function(*args, **kwargs)
        except KeyboardInterrupt, e:
            self._running = False
            self._jobs.cancel(job)
            task._errback(job, request, e)
            raise KeyboardInterrupt
        except Exception, e:
            self._jobs.retract(job)
            task._errback(job, request, e)
        else:
            self._jobs.finish(job)
            task._callback(job, request, result)

    def work_forever(self, timeout=0):
        self._running = True
        while self._running:
            self.work_once(timeout)


if __name__ == '__main__':
    import os, signal, sys

    def usage():
        print >> sys.stderr, 'Usage: python -m thoonktasks.worker <tasks_module> [<timeout>]'
        sys.exit(-1)

    if len(sys.argv) not in (2, 3):
        usage()
    
    def sighandler(signum, frame):
        os.kill(os.getpid(), signal.SIGINT)
    signal.signal(signal.SIGTERM, sighandler)

    module = sys.argv[1]
    try:
        timeout = int(sys.argv[2]) if len(sys.argv) == 3 else 0
    except ValueError:
        usage()

    __import__(module)
    try:
        print(module)
        Worker(module).work_forever(timeout)
    except KeyboardInterrupt:
        print('exiting')

#.............................................................................
#   worker.py
