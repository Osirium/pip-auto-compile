#/usr/bin/env python
import argparse
import sys
import subprocess

def compile_file(filename):
    return subprocess.check_call([sys.executable, "pip-compile", "-r", filename, "-o", filename[0:-2]+".txt", "--verbose", "--generate-hashes"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("language", nargs="+")
    parser.add_argument("language_version", nargs="+")
    parser.add_argument("files", nargs="+")

    args = parser.parse_args(sys.argv)

    for f in args.files:
        if not compile_file(f):
            return False


if __name__ == "__main__":
    exit(main())
