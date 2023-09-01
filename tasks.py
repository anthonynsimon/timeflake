import invoke


@invoke.task
def fmt(ctx, check=False):
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


@invoke.task
def publish(ctx, token=None):
    cmds = ["twine", "upload"]
    if token:
        cmds.extend(["--username", "__token__"])
        cmds.extend(["--password", token])
    cmds.append("dist/*")
    ctx.run(" ".join(cmds))
