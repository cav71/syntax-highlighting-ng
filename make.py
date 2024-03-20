#!/usr/bin/env python
"""make.py file

This is the same as a `make` file, but in python.
"""
from __future__ import annotations
import argparse
import inspect
import sys
import json
import logging
import platform
import subprocess
from pathlib import Path

log = logging.getLogger(__name__)

IMAGE = "boox"
VENV = "/venv"
APPDIR = "/app"


def run(cmd, parse=False):
    out = subprocess.check_output([str(c) for c in cmd], encoding="utf-8")
    if parse:
        if out.strip():
            return json.loads(out)
        return None
    return out


def error(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    if code:
        sys.exit(code)


def task_info():
    print(f"sys.executable: {sys.executable}")
    print(f"sys.platform: {sys.platform}")
    print(f"platform.uname().system: {platform.uname().system}")
    print(f"platform.uname().machine: {platform.uname().machine}")
    print(f"platform.uname().release: {platform.uname().release}")


def task_e2e(_):
    try:
        subprocess.check_call(
            [
                f"{VENV}/bin/aab",
                "build",
                "-t",
                "anki21",
                "-d",
                "local",
                "current",
            ],
            cwd=APPDIR,
        )
    except Exception:
        pass

    for p in sorted(Path(APPDIR).rglob("*")):
        print(f"| {p}")


def task_cross_build(args):
    "cross build an anki plugin using docker"
    if sys.platform != "win32":
        error(f"must run on windows (found '{sys.platform}')")

    p = argparse.ArgumentParser()
    p.add_argument("-n", "--info", help="run the info task", action="store_true")
    p.add_argument("--rm", help="rebuild image from scratch", action="store_true")

    options = p.parse_args(args)

    if options.rm:
        log.info("removing image '%s'", IMAGE)
        run(["docker", "image", "rm", "-f", IMAGE])

    if not run(["docker", "image", "ls", "--format", "json", IMAGE]):
        log.info("building image '%s'", IMAGE)
        run(["docker", "buildx", "build", "-t", IMAGE, "."])

    app = "info" if options.info else "e2e"
    subprocess.check_call(
        [
            "docker",
            "run",
            "-v",
            f"{str(Path.cwd())}:/app",
            "--rm",
            "-ti",
            IMAGE,
            "python",
            f"{APPDIR}/make.py",
            app,
        ]
    )


COMMANDS = {
    name[len("task_") :].replace("_", "-"): fn
    for name, fn in locals().items()
    if name.startswith("task_")
}


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    def getdoc(fn):
        return (
            fn.__doc__.strip().partition("\n")[0] if fn.__doc__ else "no help available"
        )

    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        txt = "\n".join(f"  {cmd} - {getdoc(fn)}" for cmd, fn in COMMANDS.items())
        print(  # noqa: T201
            f"""\
make.py <command> {{arguments}}

Commands:

{txt}

Running on: {sys.platform}
""",
            file=sys.stderr,
        )
        sys.exit()

    workdir = Path(__file__).parent
    if sys.argv[1] not in COMMANDS:
        error(f"cannot find the command '{sys.argv[1]}' in: {','.join(COMMANDS)}")

    function = COMMANDS[sys.argv[1]]
    n = len(inspect.signature(function).parameters)
    if n == 1:
        function(sys.argv[2:])
    elif n == 0:
        function()
    else:
        function(*sys.argv[2:])
