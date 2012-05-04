# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2012-05-04.
#=============================================================================
#   serialization.py --- 
#=============================================================================
import hashlib
import json


class SignatureError(ValueError): pass

class Serializer(object):
    
    def serialize(self, data):
        return json.dumps(data)

    def deserialize(self, message):
        return json.loads(message)


class SigningSerializer(Serializer):

    def __init__(self, key):
        self.key = key

    def _digest(self, serialized):
        sha1 = hashlib.sha1(self.key)
        sha1.update(serialized)
        return sha1.hexdigest()

    def serialize(self, data):
        serialized = super(SigningSerializer, self).serialize(data)
        message = '{0}:{1}'.format(self._digest(serialized), serialized)
        return message

    def deserialize(self, message):
        hexdigest, serialized = message.split(':', 1)
        if self._digest(serialized) != hexdigest:
            raise SignatureError(message)
        return super(SigningSerializer, self).deserialize(serialized)

#.............................................................................
#   serialization.py
