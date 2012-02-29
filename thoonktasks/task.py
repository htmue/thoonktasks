# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2012-02-29.
#=============================================================================
#   task.py --- 
#=============================================================================
from thoonk import Thoonk

from thoonktasks import _queues, _serialize


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

#.............................................................................
#   task.py
