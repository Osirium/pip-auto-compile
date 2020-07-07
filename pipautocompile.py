#/usr/bin/env python
import argparse
import sys


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("language", nargs="+")
    parser.add_argument("files", nargs="+")

    args = parser.parse(sys.argv)

    print(dir(args))
    return False


if __name__ == "__main__":
    exit(main())
