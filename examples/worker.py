import hello
from thoonktasks.worker import Worker


Worker(hello.__name__).work_forever()
