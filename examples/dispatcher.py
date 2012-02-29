# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2012-02-29.
#=============================================================================
#   dispatcher.py --- 
#=============================================================================
from Queue import Queue
from functools import partial
from threading import Thread

from thoonktasks.worker import Worker


class ParallelWorker(Worker):

    def __init__(self, num_workers, queue='default'):
        super(ParallelWorker, self).__init__(queue)
        self._num = num_workers
        self._pipe = Queue()
        for i in range(num_workers):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

    def worker(self):
        while True:
            job, dump = self._pipe.get()
            self._do_job(job, dump)
            
    def work_once(self, timeout=0):
        job, dump, _ = self._jobs.get(timeout)
        self._pipe.put((job, dump))


class Dispatcher(object):

    def __init__(self, queues, timeout=0):
        for queue, num_workers in queues:
            if num_workers == 1:
                worker = Worker(queue)
            else:
                worker = ParallelWorker(num_workers, queue)
            target = partial(worker.work_forever, timeout)
            t = Thread(target=target)
            t.daemon = True
            t.start()
        self._stop = Queue()

    def work_forever(self):
        self._stop.get()

#.............................................................................
#   dispatcher.py
