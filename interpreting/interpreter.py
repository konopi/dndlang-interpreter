from io import TextIOWrapper
from lexing.lexer import Lexer
from parsing.parser import Parser
from interpreting.scope import Scope
from interpreting.error_handling import InterpreterError, ArgumentError, MultipleNameError, UndeclaredVariableError

class Interpreter:
    def __init__(self, io: TextIOWrapper):
        self.lexer = Lexer(io)
        self.parser = Parser(self.lexer)
        self.parsing_error = False
        self.ast = self.parser.parse()
        if self.ast == -1:
            self.parsing_error = True
            return
        self.scope = Scope()
        self.load_function_definitions()

    def execute(self):
        if self.parsing_error:
            return -1
        for instruction in self.ast.instructions:
            try:
                instruction.execute(self.scope)

            except TypeError:
                print(InterpreterError(e_type = "TypeError", msg = "Attempted arithmetic operation on unsupported type", line_no = instruction.line_no))
                return -1
            except RecursionError:
                print(InterpreterError(e_type = "RecursionError", msg = "Recursion limit exceeded", line_no = instruction.line_no))
                return -1
            except ArgumentError as e:
                print(InterpreterError(e_type = "ArgumentError", msg = "Function call missing " + str(e.missing_argument_count) \
                                     + " argument" + ('s' if e.missing_argument_count > 1 else ''), line_no = instruction.line_no))
                return -1
            except NameError as e:
                print(InterpreterError(e_type = "NameError", msg = "Name '" + e.args[0] + "' is not defined", line_no = instruction.line_no))
                return -1
            except MultipleNameError as e:
                print(InterpreterError(e_type = "MultipleNameError", msg = "Name '" + e.args[0] + "' is already defined", line_no = instruction.line_no))
                return -1
            except UndeclaredVariableError as e:
                print(InterpreterError(e_type = "UndeclaredVariableError", msg = "Variable '" + e.args[0] + "' is not declared", line_no = instruction.line_no))
                return -1
        return 0

    def load_function_definitions(self):
        for function in self.ast.functions:
            self.scope.add_definition(function)

    def print_ast(self):
        print("Instructions:")
        for i in self.ast.instructions:
            print(i)
        print("Functions:")
        for f in self.ast.functions:
            print(f)
        print("Templates:")
        for t in self.ast.templates:
            print(t)
        print()
