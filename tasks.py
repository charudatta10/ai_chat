from invoke import task

@task
def run(c):
    c.run("python -m app")