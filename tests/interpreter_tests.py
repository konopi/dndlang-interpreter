import unittest
import sys
sys.path.append('D:\Projects\dndlang-python')
from interpreting.interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    
    def test_hello_world(self):
        fname = r'test_cases\hello_world.adv'
        try:
            file = open(fname, 'r')
            interpreter = Interpreter(file)
            interpreter.execute()
        except OSError:
            self.fail("Couldn't open test file: " + fname)
        finally:
            file.close()
    def test_string_return(self):
        fname = r'test_cases\string_return.adv'
        try:
            file = open(fname, 'r')
            interpreter = Interpreter(file)
            interpreter.execute()
        except OSError:
            self.fail("Couldn't open test file: " + fname)
        finally:
            file.close()
    def test_simple_functions(self):
        fname = r'test_cases\simple_functions.adv'
        try:
            file = open(fname, 'r')
            interpreter = Interpreter(file)
            interpreter.execute()
        except OSError:
            self.fail("Couldn't open test file: " + fname)
        finally:
            file.close()
    def test_fibonacci(self):
        fname = r'test_cases\fibonacci.adv'
        try:
            file = open(fname, 'r')
            interpreter = Interpreter(file)
            interpreter.execute()
        except OSError:
            self.fail("Couldn't open test file: " + fname)
        finally:
            file.close()
    def test_power(self):
        fname = r'test_cases\power.adv'
        try:
            file = open(fname, 'r')
            interpreter = Interpreter(file)
            interpreter.execute()
        except OSError:
            self.fail("Couldn't open test file: " + fname)
        finally:
            file.close()
    def test_dice_functions(self):
        fname = r'test_cases\dice_functions.adv'
        try:
            file = open(fname, 'r')
            interpreter = Interpreter(file)
            interpreter.execute()
        except OSError:
            self.fail("Couldn't open test file: " + fname)
        finally:
            file.close()
if __name__ == '__main__':
    unittest.main()
