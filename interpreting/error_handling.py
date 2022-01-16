
class InterpreterError:
    def __init__(self, e_type: str = "Error", msg: str = "Something went wrong", line_no: int = 0):
        self.e_type = e_type
        self.msg = msg
        self.line_no = line_no
    def __str__(self):
        line_msg = str(self.line_no) if self.line_no != 0 else "who knows which"
        return self.e_type + ": " + self.msg + ", line " + line_msg

class ArgumentError(Exception):
    '''Incorrect arguments.'''
    def __init__(self, missing_argument_count: int = 0):
        super(ArgumentError, self).__init__()
        self.missing_argument_count = missing_argument_count
class MultipleNameError(Exception):
    '''Multiple instances of the same name found.'''
    pass
class UndeclaredVariableError(Exception):
    '''Attempted to use an undeclared variable.'''
    pass
