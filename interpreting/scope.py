from interpreting.error_handling import MultipleNameError, UndeclaredVariableError

class Scope:
    def __init__(self) -> None:
        self.variables = {}
        self.definitions = {}

    def add_variable(self, name: str) -> None:
        if name not in self.variables:
            self.variables[name] = None
        else:
            # variable already declared
            raise MultipleNameError(name)
    def set_variable_value(self, name: str, value) -> None:
        if name in self.variables:
            self.variables[name] = value
        else:
            # undeclared variable
            raise UndeclaredVariableError(name)
    def get_variable_value(self, name: str):
        if name in self.variables:
            return self.variables[name]
        else:
            # undeclared variable
            raise UndeclaredVariableError(name)

    def add_definition(self, function) -> None:
        if function.name not in self.definitions:
            self.definitions[function.name] = function
        else:
            # function already declared
            raise MultipleNameError(function.name)
