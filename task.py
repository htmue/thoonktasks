import json

from thoonk import Thoonk


_queues = dict()


_serialize = json.dumps
_deserialize = json.loads


def task(queue='default', priority=False):
    def task(function):
        return Task(function, queue, priority)
    return task
            

class Task(object):
    _thoonk = Thoonk('127.0.0.1', 6379)
    
    def __init__(self, function, queue='default', priority=False):
        self._function = function
        self._name = '{0}:{1}'.format(function.__module__, function.__name__)
        self._queue = queue
        self._priority = priority
        self._jobs = self._thoonk.job(self._queue)
        _queues.setdefault(queue, {})[self._name] = self

    def __call__(self, *args, **kwargs):
        self._jobs.put(_serialize([self._name, args, kwargs]))


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
