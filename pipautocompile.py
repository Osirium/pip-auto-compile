#/usr/bin/env python
import argparse
import sys
from piptools.scripts import compile
from piptools.exceptions import PipToolsError

def compile_file(filename, pip_args):
    compile.cli(["-r", filename, "-o", filename[0:-2]+"txt", "--verbose", "--generate-hashes"]+pip_args)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip-compile-arg", action="append")
    parser.add_argument("files", nargs="+")

    args = parser.parse_args(sys.argv)

    files = args.files[1:]
    pip_args = []
    if ( args.pip_compile_arg):
        pip_args = args.pip_compile_arg

    for f in files:
        if f.endswith(".txt"):
            # Attempt to find a matching in file if we changed a requirements.txt
            requirementsin = f[0:-3]+"in"
            if requirementsin not in files:
                try:
                    print("Compiling {}".format(requirementsin))
                    compile_file(requirementsin, pip_args)
                except SystemExit as e:
                    if (e.code != 0):
                        print("Attempted to compile maching `.in` to {}".format(f))
                        print("Could not compile {}".format(requirementsin))
                        print("Perhaps {} doesnt exist".format(requirementsin))
                    continue
        else:
            print("non txt file")
            try:
                compile_file(f, pip_args)
            except SystemExit as e:
                if (e.code != 0):
                    print(e)
                    print("Could not compile {}".format(f))
                    return False
                continue

if __name__ == "__main__":
    main()
