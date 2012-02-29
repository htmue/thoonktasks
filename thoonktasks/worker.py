# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2012-02-29.
#=============================================================================
#   worker.py --- 
#=============================================================================
from thoonk import Thoonk

from thoonktasks import _queues, _deserialize


class Worker(object):
    _thoonk = Thoonk('127.0.0.1', 6379)

    def __init__(self, queue='default'):
        self._queue = queue
        self._jobs = self._thoonk.job(self._queue)
        
    def work_once(self, timeout=0):
        job, dump, _ = self._jobs.get(timeout)
        self._do_job(job, dump)

    def _do_job(self, job, dump):
        self._call(dump)
        self._jobs.finish(job)

    def work_forever(self, timeout=0):
        while True:
            self.work_once(timeout)
    
    def _call(self, dump):
        name, args, kwargs = _deserialize(dump)
        task = _queues[self._queue][name]
        task._function(*args, **kwargs)


#.............................................................................
#   worker.py
