from thoonktasks.task import task


@task(__name__)
def hello(you='world'):
    print('Hello {}!'.format(you))

@hello.callback
def hello_callback(task, job, request, result):
    print request, 'succeeded'
