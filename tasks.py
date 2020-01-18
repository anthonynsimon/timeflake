import invoke


@invoke.task
def test(ctx):
    ctx.run('pytest -v -s')

@invoke.task
def benchmark(ctx):
    ctx.run('python benchmark/benchmark.py')

@invoke.task
def build(ctx):
    ctx.run('python setup.py clean')
    ctx.run('python setup.py sdist bdist_wheel')

@invoke.task
def publish(ctx):
    ctx.run('twine upload dist/*')
