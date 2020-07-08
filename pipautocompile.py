#/usr/bin/env python
import sys
from piptools.scripts import compile

def compile_file(filename):
    return compile.cli(["-r", filename, "-o", filename[0:-2]+"txt", "--verbose", "--generate-hashes"])

def main():
    files = sys.argv[1:]

    for f in files:
        if not compile_file(f):
            return False


if __name__ == "__main__":
    exit(main())
