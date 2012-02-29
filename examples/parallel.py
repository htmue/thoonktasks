import hello
from dispatcher import Dispatcher


Dispatcher([(hello.__name__, 3)]).work_forever()
