# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2012-02-29.
#=============================================================================
#   __init__.py --- 
#=============================================================================
import os

from thoonk import Thoonk

from thoonktasks.serialization import Serializer


_queues = dict()

class BaseObject(object):
    _thoonk = Thoonk(
        os.environ.get('THOONK_HOST', '127.0.0.1'),
        int(os.environ.get('THOONK_PORT', 6379)),
        int(os.environ.get('THOONK_DB', 0)),
    )

    @classmethod
    def set_serializer(self, serializer):
        self._serializer = serializer
    
    @classmethod
    def serialize(self, data):
        return self._serializer.serialize(data)
    
    @classmethod
    def deserialize(self, message):
        return self._serializer.deserialize(message)


def set_serializer(serializer):
    BaseObject.set_serializer(serializer)

set_serializer(Serializer())

#.............................................................................
#   __init__.py
