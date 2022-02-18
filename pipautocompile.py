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
    output_filename = str(filename.with_suffix(".txt").name)
    with chdir(filename.parent):
        try:
            compile.cli(
                pip_args
                + [
                    "-o",
                    output_filename,
                    "--verbose",
                    "--generate-hashes",
                    "--",
                    str(filename.name),
                ]
            )
            return 0
        except SystemExit as e:
            if e.code != 0:
                print(e)
                print("Could not compile {}".format(filename))
            else:
                # forces all end lines to be '\n'
                with open(output_filename, 'rb') as f:
                    output_content = f.read()
                fixed_content = b''.join(
                    line.rstrip(b'\r\n') + b'\n' for line in output_content.splitlines(True)
                )
                with open(output_filename, 'wb') as f:
                    f.write(fixed_content)
            return e.code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")

    args, other_args = parser.parse_known_args(sys.argv[1:])
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    files = sorted({pathlib.Path(p).with_suffix(".in") for p in args.files})

    with lock:
        return max(compile_file(f, other_args) for f in files)


if __name__ == "__main__":
    sys.exit(main())
