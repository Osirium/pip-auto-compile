#/usr/bin/env python
import sys
from piptools.scripts import compile
from piptools.exceptions import PipToolsError

def monkey_exit(val):
    ''' pip.compile.cli is not meant to be called by a script.
        So it calls sys.exit() when its done, or on error, 
        which kills the script before we can finish nicely.
        Better turn that exit() into an exception that we can catch instead
    '''
    if( val != 0 and val is not None ):
        raise PipToolsError(val)
    return

compile.sys.exit = monkey_exit

def compile_file(filename):
    compile.cli(["-r", filename, "-o", filename[0:-2]+"txt", "--verbose", "--generate-hashes"])

def main():
    files = sys.argv[1:]
    print(files)

    for f in files:
        if f.endswith(".txt"):
            # Attempt to find a matching in file if we changed a requirements.txt
            requirementsin = f[0:-3]+"in"
            if requirementsin not in files:
                try:
                    print("Compiling {}".format(requirementsin))
                    compile_file(requirementsin)
                except PipToolsError:
                    print("Attempted to compile maching `.in` to {}".format(f))
                    print("Could not compile {}".format(requirementsin))
                    print("Perhaps {} doesnt exist".format(requirementsin))
                    continue
        else:
            print("non txt file")
            try:
                compile_file(f)
            except PipToolsError as e:
                print(e)
                print("Could not compile {}".format(f))
                return False

if __name__ == "__main__":
    main()
