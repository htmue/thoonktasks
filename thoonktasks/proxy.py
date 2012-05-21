# -*- coding:utf-8 -*-
# Copyright 2012 Hans-Thomas Mueller
# Distributed under the terms of the GNU General Public License v2
#=============================================================================
#   proxy.py --- Task proxy for avoiding imports in some cases
#=============================================================================
from thoonktasks import _queues
from thoonktasks.task import Task


def proxy(name, queue='default', priority=False, module=None):
    return Proxy(name, queue, priority, queue if module is None else module)

class Proxy(Task):

    def __init__(self, name, queue='default', priority=False, module=None):
        self._name = '{0}:{1}'.format(module, name)
        self._queue = queue
        self._priority = priority
        self._jobs = self._thoonk.job(self._queue)
        _queues.setdefault(queue, {})[self._name] = self
    
    def _function(self, *args, **kwargs):
        raise RuntimeError('proxy object, cannot call worker function')

#.............................................................................
#   proxy.py
