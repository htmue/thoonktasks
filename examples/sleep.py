import sys
import time

from thoonktasks.task import task


@task(__name__)
def sleep(timeout=1):
    print 'Sleeping for {} second(s)'.format(timeout)
    for i in range(timeout):
        time.sleep(1)
        print '.',
        sys.stdout.flush()
    print 'done.'
