# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2012-02-29.
#=============================================================================
#   __init__.py --- 
#=============================================================================
import json
import os

from thoonk import Thoonk


_queues = dict()
_serialize = json.dumps
_deserialize = json.loads
_thoonk = Thoonk(
    os.environ.get('THOONK_HOST', '127.0.0.1'),
    int(os.environ.get('THOONK_PORT', 6379)),
    int(os.environ.get('THOONK_DB', 0)),
)

#.............................................................................
#   __init__.py
