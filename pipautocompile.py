# /usr/bin/env python
import argparse
import contextlib
import os
import sys

try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

from piptools.scripts import compile
from piptools.exceptions import PipToolsError


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
            [
                "-r",
                str(filename),
                "-o",
                str(filename.with_suffix(".txt")),
                "--verbose",
                "--generate-hashes",
            ]
            + pip_args
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip-compile-arg", action="append")
    parser.add_argument("files", nargs="+")

    args = parser.parse_args(sys.argv)

    files = sorted({pathlib.Path(p).with_suffix(".in") for p in args.files[1:]})
    pip_args = []
    if args.pip_compile_arg:
        pip_args = args.pip_compile_arg

    for f in files:
        try:
            compile_file(f, pip_args)
        except SystemExit as e:
            if e.code != 0:
                print(e)
                print("Could not compile {}".format(f))
                return False
            continue


if __name__ == "__main__":
    main()
