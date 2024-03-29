# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2012-02-29.
#=============================================================================
#   task.py --- Task queue decorator
#=============================================================================
import logging

from thoonktasks import _queues, BaseObject


def task(queue='default', priority=False):
    def task(function):
        return Task(function, queue, priority)
    return task


class Task(BaseObject):
    log = logging.getLogger(__name__)
    _custom_callback = None
    _custom_errback = None
    
    def __init__(self, function, queue='default', priority=False):
        self._function = function
        self._name = '{0}:{1}'.format(function.__module__, function.__name__)
        self._queue = queue
        self._priority = priority
        self._jobs = self._thoonk.job(self._queue)
        _queues.setdefault(queue, {})[self._name] = self
    
    def __call__(self, *args, **kwargs):
        self._jobs.put(self.serialize([self._name, args, kwargs]))
    
    def _callback(self, job, request, result):
        if self._custom_callback is None:
            self.default_callback(job, request, result)
        else:
            self._custom_callback(self, job, request, result)
    
    def _errback(self, job, request, e):
        if self._custom_errback is None:
            self.default_errback(job, request, e)
        else:
            self._custom_errback(self, job, request, e)
    
    def default_callback(self, job, request, result):
        self.log.info('%s:%s -> %s', job, self._serializer.deserialize(request), repr(result))
    
    def default_errback(self, job, request, e):
        self.log.error('%s:%s -> %s', job, self._serializer.deserialize(request), repr(e))
    
    def callback(self, function):
        self._custom_callback = function
    
    def errback(self, function):
        self._custom_errback = function
    
    def flush_queue(self):
        for id in self._jobs.get_ids():
            self._jobs.retract(id)

#.............................................................................
#   task.py
