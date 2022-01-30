import invoke


@invoke.task
def fmt(ctx, check=True):
    cmd = "black --check ." if check else "black ."
    ctx.run(cmd)


@invoke.task
def test(ctx):
    ctx.run("pytest -v -s")


@invoke.task
def benchmark(ctx):
    ctx.run("python benchmark/benchmark.py")


@invoke.task
def clean(ctx):
    ctx.run("rm -rf dist")
    ctx.run("python setup.py clean --all")


@invoke.task(clean)
def build(ctx):
    ctx.run("python setup.py sdist bdist_wheel")


@invoke.task(fmt, test, build)
def publish(ctx):
    ctx.run("twine upload dist/*")
