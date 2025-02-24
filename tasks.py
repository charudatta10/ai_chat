from invoke import task, Collection

@task
def run(c):
    c.run("python -m app")

@task
def test(c):
    c.run("pytest")

Collection(run, test).add_task(test, name='default')