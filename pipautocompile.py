# /usr/bin/env python
import argparse
import contextlib
import filelock
import os
import sys

try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

from piptools.locations import CACHE_DIR
from piptools.exceptions import PipToolsError
from piptools.scripts import compile


LOCK_PATH = pathlib.Path(CACHE_DIR) / ".pip-auto-compile.lock"
lock = filelock.FileLock(str(LOCK_PATH))

@contextlib.contextmanager
def chdir(path):
    old_wd = pathlib.Path.cwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(str(old_wd))


def compile_file(filename, pip_args):
    with chdir(filename.parent):
        compile.cli(
            pip_args + 
            [
                "-o",
                str(filename.with_suffix(".txt").name),
                "--verbose",
                "--generate-hashes",
                "--",
                str(filename.name),
            ]
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")

    args, other_args = parser.parse_known_args(sys.argv[1:])
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    files = sorted({pathlib.Path(p).with_suffix(".in") for p in args.files})

    with lock:
        for f in files:
            try:
                compile_file(f, other_args)
            except SystemExit as e:
                if e.code != 0:
                    print(e)
                    print("Could not compile {}".format(f))
                    return False

if __name__ == "__main__":
    main()
