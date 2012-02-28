from task import task

@task()
def hello(you='world'):
    print('Hello {}!'.format(you))
