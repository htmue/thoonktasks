import hello
from task import Worker


Worker(hello.__name__).work_forever()
