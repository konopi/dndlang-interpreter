from interpreting.interpreter import Interpreter
import sys
import argparse

argparser = argparse.ArgumentParser(description="Run dndlang interpreter with filename")
argparser.add_argument('filename', metavar = 'FILE_PATH', type=str)
args = argparser.parse_args()
fname = args.filename

try:
    file = open(fname, 'r')
    interpreter = Interpreter(file)
    interpreter.execute()
except OSError:
    print("Could not open file: " + fname)
    sys.exit()
finally:
    file.close()
