from dispatcher import Dispatcher,  ParallelWorker
import hello

# ParallelWorker(3).work_forever()
Dispatcher([('default', 3)]).work_forever()
