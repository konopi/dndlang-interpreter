from interpreting.error_handling import ArgumentError

class Node():
    pass

from interpreting.scope import Scope
class Instruction(Node):
    # line_no
    def execute(self, scope: Scope):
        raise NotImplementedError()
class Declaration(Instruction):
    # var_type, var
    def execute(self, scope: Scope):
        scope.add_variable(self.var.name)
class Assignment(Instruction):
    # lhs, rhs
    def execute(self, scope: Scope):
        scope.set_variable_value(self.lhs.name, self.rhs.evaluate(scope))
class AttackMove(Instruction):
    # attacker, defender
    def execute(self, scope: Scope):
        pass
class While(Instruction):
    # condition, block
    def execute(self, scope: Scope):
        while self.condition.evaluate(scope):
            for instruction in self.block.instructions:
                instruction.execute(scope)
class If(Instruction):
    # condition, if_block, else_block
    def execute(self, scope: Scope):
        if self.condition.evaluate(scope):
            for instruction in self.if_block.instructions:
                result = instruction.execute(scope)
                if result is not None:
                    return result
        elif self.else_block is not None:
            for instruction in self.else_block.instructions:
                result = instruction.execute(scope)
                if result is not None:
                    return result
class Condition(Node):
    # first_operand, operator, second_operand
    def evaluate(self, scope: Scope) -> bool:
        if self.operator == TokenType.LESS_THAN:
            return self.first_operand.evaluate(scope) < self.second_operand.evaluate(scope)
        elif self.operator == TokenType.MORE_THAN:
            return self.first_operand.evaluate(scope) > self.second_operand.evaluate(scope)
        elif self.operator == TokenType.LESS_OR_EQUAL:
            return self.first_operand.evaluate(scope) <= self.second_operand.evaluate(scope)
        elif self.operator == TokenType.MORE_OR_EQUAL:
            return self.first_operand.evaluate(scope) >= self.second_operand.evaluate(scope)
        elif self.operator == TokenType.EQUALS:
            return self.first_operand.evaluate(scope) == self.second_operand.evaluate(scope)
class Log(Instruction):
    # value
    def execute(self, scope: Scope):
        if isinstance(self.value, Variable):
            print( scope.get_variable_value( self.value.evaluate(scope) ) )
        else:
            print( self.value.evaluate(scope) )
class Return(Instruction):
    # value
    def execute(self, scope: Scope):
        return self.value.evaluate(scope)

class FunctionDefinition(Node):
    # name, block
    def __init__(self):
        super(FunctionDefinition, self).__init__()
        self.parameters = []
class InstructionBlock(Node):
    def __init__(self):
        super(InstructionBlock, self).__init__()
        self.instructions = []

from recordtype import recordtype
from lexing.token import TokenType
CharacterAttribute = recordtype('CharacterAttribute', 'value increase_type increase_amount')

class Template(Node):
    # name, health, attack, defence
    pass
class Item(Template):
    # desc, value
    pass
class Character(Template):
    # level, reqexp, exp, equipped, inventory, reward
    pass

class Assignable(Node):
    pass

class Literal(Assignable):
    pass
class Number(Literal):
    def __init__(self, value: str):
        super(Number, self).__init__()
        self.value = int(value)
    def evaluate(self, scope):
        return self.value
class String(Literal):
    def __init__(self, value: str):
        super(String, self).__init__()
        self.value = value
    def evaluate(self, scope):
        return self.value
from random import randint
class Dice(Literal):
    def __init__(self, number: int, faces: int):
        super(Dice, self).__init__()
        self.number = number
        self.faces = faces
    def __init__(self, string: str):
        super(Dice, self).__init__()
        values = string.split('d')
        self.number = int(values[0])
        self.faces = int(values[1])
    def evaluate(self, scope: Scope):
        return self
    def roll(self) -> int:
        result = 0
        for i in range(self.number):
            result += randint(1, self.faces)
        return result
    def __str__(self) -> str:
        return "%sd%s" % (self.number, self.faces)

class Expression(Assignable):
    def __init__(self):
        super(Expression, self).__init__()
        self.operands = []
        self.operators = []
    def add_operand(self, operand):
        self.operands.append(operand)
    def add_operator(self, operator):
        self.operators.append(operator)
    def push(self, op):
        self.stack.append(op)
    def evaluate(self, scope: Scope):
        if len(self.operators) == 0:
            result = self.operands[0]
            if result is not None:
                return result.evaluate(scope)
        else:
            evaluated_value = self.operands[0].evaluate(scope)
            if not isinstance(evaluated_value, (int, float)): raise TypeError(self.operands[0])
            i = 1
            for operator in self.operators:
                next_value = self.operands[i].evaluate(scope)
                if not isinstance(next_value, (int, float)): raise TypeError(self.operands[i])
                if operator == TokenType.PLUS:
                    evaluated_value += next_value
                elif operator == TokenType.MINUS:
                    evaluated_value -= next_value
                elif operator == TokenType.ASTERISK:
                    evaluated_value *= next_value
                elif operator == TokenType.SLASH:
                    evaluated_value /= next_value
                i += 1
            return evaluated_value

class FunctionCall(Instruction, Assignable):
    def __init__(self, name: str):
        super(FunctionCall, self).__init__()
        self.name = name
        self.arguments = []
    def evaluate(self, scope: Scope):
        if self.name in scope.definitions:
            definition = scope.definitions[self.name]
            if len(self.arguments) != len(definition.parameters):
                # argument count doesn't match
                raise ArgumentError(abs(len(self.arguments) - len(definition.parameters)))
            else:
                function_scope = Scope()
                function_scope.definitions = scope.definitions
                i = 0
                for argument in self.arguments:
                    var = definition.parameters[i]
                    function_scope.add_variable(var.name)
                    function_scope.set_variable_value(var.name, argument.evaluate(scope))
                    i += 1
                for instruction in definition.block.instructions:
                    result = instruction.execute(function_scope)
                    if result is not None:
                        return result
        else:
            # function not defined
            raise NameError(self.name)
    def execute(self, scope: Scope):
        self.evaluate(scope)
class Variable(Assignable):
    def __init__(self, name: str):
        super(Variable, self).__init__()
        self.name = name
    def evaluate(self, scope: Scope):
        return scope.get_variable_value(self.name)

class DiceRoll(Expression):
    def __init__(self, operand):
        super(DiceRoll, self).__init__()
        self.operand = operand
    def evaluate(self, scope):
        if isinstance(self.operand, Dice):
            return self.operand.roll()
        elif isinstance(self.operand, Variable):
            return self.operand.evaluate(scope).roll()

class Program(Node):
    def __init__(self):
        super(Program, self).__init__()
        self.templates = []
        self.functions = []
        self.instructions = []

    def add(self, node: Node):
        if isinstance(node, Instruction):
            self.add_instruction(node)
        elif isinstance(node, Template):
            self.add_template(node)
        elif isinstance(node, FunctionDefinition):
            self.add_function(node)

    def add_instruction(self, instruction: Instruction):
        self.instructions.append(instruction)
    def add_template(self, template: Template):
        self.templates.append(template)
    def add_function(self, function: FunctionDefinition):
        self.functions.append(function)
