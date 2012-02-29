from task import task

@task(__name__)
def hello(you='world'):
    print('Hello {}!'.format(you))
