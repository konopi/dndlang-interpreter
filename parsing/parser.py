import sys

from lexing.lexer import Lexer
from lexing.token import Token, TokenType
from . import error_handling, ast

class Parser():
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.buffered_token = None
    
    def parse(self):
        self.buffered_token = None

        syntax_tree = ast.Program()

        while(statement := self.parse_statement()):
            syntax_tree.add(statement)

        return syntax_tree

    def is_acceptable(self, token: Token, acceptable: tuple) -> bool:
        for token_type in acceptable:
            if token.t_type == token_type:
                return True
        return False

    def accept(self, acceptable: tuple) -> Token:
        if self.buffered_token is None:
            token = self.lexer.next_token()
        else:
            token = self.buffered_token
            self.buffered_token = None
        
        try:
            if self.is_acceptable(token, acceptable):
                return token
            else:
                raise error_handling.UnexpectedTokenError("UnexpectedTokenError: expected: " + str(acceptable) \
                                                        + "; got: " + str(token.t_type) + " '" + token.t_value + "', line " \
                                                        + str(self.lexer.reader.position.line_no) + ", char " + str(self.lexer.reader.position.char_no))
        except error_handling.UnexpectedTokenError as e:
            print(e)
            sys.exit()

    def peek(self, acceptable: tuple) -> bool:
        if self.buffered_token is None:
            self.buffered_token = self.lexer.next_token()
        return self.is_acceptable(self.buffered_token, acceptable)

    def parse_statement(self) -> ast.Node:
        token = self.accept(( TokenType.ITEM, TokenType.CHARACTER, TokenType.FUNCTION, TokenType.IDENTIFIER, \
                              TokenType.WHILE, TokenType.IF, TokenType.QUESTION_MARK, TokenType.RETURN, TokenType.END_OF_FILE ))

        result = None
        if token.t_type == TokenType.ITEM:
            result = self.parse_item()
        elif token.t_type == TokenType.CHARACTER:
            result = self.parse_character()
        elif token.t_type == TokenType.FUNCTION:
            result = self.parse_function_definition()
        elif token.t_type in (TokenType.IDENTIFIER, TokenType.WHILE, TokenType.IF, TokenType.QUESTION_MARK, TokenType.RETURN):
            result = self.parse_instruction(token)
        elif token.t_type == TokenType.END_OF_FILE:
            result = None

        return result

    def parse_item(self) -> ast.Item:
        result = ast.Item()

        token = self.accept(( TokenType.IDENTIFIER, ))
        result.name = token.t_value

        self.accept(( TokenType.CURLY_OPEN, ))
        while self.peek(( TokenType.HEALTH, TokenType.ATTACK, TokenType.DEFENCE, TokenType.DESC, TokenType.VALUE )):

            attribute_token = self.accept(( TokenType.HEALTH, TokenType.ATTACK, TokenType.DEFENCE, TokenType.DESC, TokenType.VALUE ))
            self.accept(( TokenType.COLON, ))
            if attribute_token.t_type in { TokenType.HEALTH, TokenType.ATTACK, TokenType.DEFENCE, TokenType.VALUE }:
                attribute_value = self.parse_number()
            elif attribute_token.t_type in { TokenType.DESC }:
                attribute_value = self.parse_string()

            if attribute_token.t_type == TokenType.HEALTH:
                result.health = attribute_value
            elif attribute_token.t_type == TokenType.ATTACK:
                result.attack = attribute_value
            elif attribute_token.t_type == TokenType.DEFENCE:
                result.defence = attribute_value
            elif attribute_token.t_type == TokenType.DESC:
                result.desc = attribute_value
            elif attribute_token.t_type == TokenType.VALUE:
                result.value = attribute_value

        self.accept(( TokenType.CURLY_CLOSE, ))

        return result

    def parse_character(self) -> ast.Character:
        result = ast.Character()

        token = self.accept(( TokenType.IDENTIFIER, ))
        result.name = token.t_value

        self.accept(( TokenType.CURLY_OPEN, ))

        while self.peek(( TokenType.HEALTH, TokenType.ATTACK, TokenType.DEFENCE, TokenType.LEVEL, TokenType.REQEXP, \
                          TokenType.EXP, TokenType.EQUIPPED, TokenType.INVENTORY, TokenType.REWARD )):

            attribute_token = self.accept(( TokenType.HEALTH, TokenType.ATTACK, TokenType.DEFENCE, TokenType.LEVEL, TokenType.REQEXP, \
                                            TokenType.EXP, TokenType.EQUIPPED, TokenType.INVENTORY, TokenType.REWARD ))
            self.accept(( TokenType.COLON, ))
            if attribute_token.t_type in { TokenType.HEALTH, TokenType.ATTACK, TokenType.DEFENCE, TokenType.LEVEL, TokenType.REQEXP, TokenType.EXP }:
                attribute_value = self.parse_character_stat()
            elif attribute_token.t_type in { TokenType.EQUIPPED, TokenType.INVENTORY, TokenType.REWARD }:
                attribute_value = self.parse_item_set()

            if attribute_token.t_type == TokenType.HEALTH:
                result.health = attribute_value
            elif attribute_token.t_type == TokenType.ATTACK:
                result.attack = attribute_value
            elif attribute_token.t_type == TokenType.DEFENCE:
                result.defence = attribute_value
            elif attribute_token.t_type == TokenType.LEVEL:
                result.level = attribute_value
            elif attribute_token.t_type == TokenType.REQEXP:
                result.reqexp = attribute_value
            elif attribute_token.t_type == TokenType.EXP:
                result.exp = attribute_value

            elif attribute_token.t_type == TokenType.EQUIPPED:
                result.equipped = attribute_value
            elif attribute_token.t_type == TokenType.INVENTORY:
                result.inventory = attribute_value
            elif attribute_token.t_type == TokenType.REWARD:
                result.reward = attribute_value

        self.accept(( TokenType.CURLY_CLOSE, ))

        return result

    def parse_character_stat(self) -> ast.CharacterAttribute:
        value_token = self.accept(( TokenType.NUMBER_LITERAL, ))

        if self.peek(( TokenType.INCREASES_BY, TokenType.MULTIPLIES_BY )):
            increase_type_token = self.accept(( TokenType.INCREASES_BY, TokenType.MULTIPLIES_BY ))
            increase_amount_token = self.accept(( TokenType.NUMBER_LITERAL, TokenType.DICE_LITERAL ))
            result = ast.CharacterAttribute(int(value_token.t_value), increase_type_token.t_type, increase_amount_token.t_value)
        else:
            result = ast.CharacterAttribute(int(value_token.t_value), None, None)

        return result

    def parse_item_set(self) -> list:
        item_set = []
        end = False
        while not end:
            item_name = self.accept(( TokenType.IDENTIFIER, ))
            if self.peek(( TokenType.SLASH, TokenType.AND )):
                separator = self.accept(( TokenType.SLASH, TokenType.AND ))
                if separator.t_type == TokenType.SLASH:
                    item_amount = self.accept(( TokenType.NUMBER_LITERAL, ))
                    item_set.append( (item_name.t_value, int(item_amount.t_value)) )
                    if self.peek(( TokenType.AND, )):
                        self.accept(( TokenType.AND, ))
                    else:
                        end = True
                elif separator.t_type == TokenType.AND:
                    item_set.append( (item_name.t_value, 1) )
            else:
                item_set.append( (item_name.t_value, 1) )
                end = True
        return item_set

    def parse_function_definition(self) -> ast.FunctionDefinition:
        result = ast.FunctionDefinition()
        name_token = self.accept(( TokenType.IDENTIFIER, ))
        result.name = name_token.t_value
        result.parameters = self.parse_definition_parameters()
        result.block = self.parse_instruction_block()
        return result

    def parse_definition_parameters(self) -> list:
        result = []
        self.accept(( TokenType.ROUND_OPEN, ))
        while not self.peek(( TokenType.ROUND_CLOSE, )):
            parameter = self.parse_variable()
            result.append(parameter)
            if self.peek(( TokenType.COMMA, )):
                self.accept(( TokenType.COMMA, ))
        self.accept(( TokenType.ROUND_CLOSE, ))
        return result

    def parse_instruction_block(self) -> ast.InstructionBlock:
        result = ast.InstructionBlock()
        self.accept(( TokenType.CURLY_OPEN, ))
        while not self.peek(( TokenType.CURLY_CLOSE, )):
            result.instructions.append(self.parse_instruction())
        self.accept(( TokenType.CURLY_CLOSE, ))
        return result

    def parse_instruction(self, token: Token = None) -> ast.Instruction:
        line_no = self.lexer.reader.position.line_no
        if token is None:
            token = self.accept(( TokenType.IDENTIFIER, TokenType.WHILE, TokenType.IF, TokenType.QUESTION_MARK, TokenType.RETURN ))
        if token.t_type == TokenType.IDENTIFIER:
            result = self.parse_assignment_or_call_or_declaration_or_attack_move(token)
            self.accept(( TokenType.SEMICOLON, ))
        elif token.t_type == TokenType.WHILE:
            result = self.parse_while()
        elif token.t_type == TokenType.IF:
            result = self.parse_if()
        elif token.t_type == TokenType.QUESTION_MARK:
            result = self.parse_log()
            self.accept(( TokenType.SEMICOLON, ))
        elif token.t_type == TokenType.RETURN:
            result = self.parse_return()
            self.accept(( TokenType.SEMICOLON, ))
        result.line_no = line_no
        return result

    def parse_assignment_or_call_or_declaration_or_attack_move(self, token: Token) -> ast.Instruction:
        if self.peek(( TokenType.ASSIGN, )):
            return self.parse_assignment(token)
        elif self.peek(( TokenType.ROUND_OPEN, )):
            return self.parse_function_call(token)
        elif self.peek(( TokenType.IDENTIFIER, )):
            return self.parse_declaration(token)
        elif self.peek(( TokenType.ATTACK_MOVE, )):
            return self.parse_attack_move(token)

    def parse_assignment(self, identifier: Token) -> ast.Assignment:
        result = ast.Assignment()
        self.accept(( TokenType.ASSIGN, ))
        result.lhs = ast.Variable(identifier.t_value)
        result.rhs = self.parse_assignable()
        return result

    def parse_declaration(self, identifier: Token) -> ast.Declaration:
        result = ast.Declaration()
        result.var_type = identifier.t_value
        result.var = self.parse_variable()
        return result

    def parse_attack_move(self, identifier: Token) -> ast.AttackMove:
        result = ast.AttackMove()
        result.attacker = ast.Variable(identifier.t_value)
        self.accept(( TokenType.ATTACK_MOVE, ))
        result.defender = self.parse_variable()
        return result

    def parse_while(self) -> ast.While:
        result = ast.While()
        result.condition = self.parse_condition()
        result.block = self.parse_instruction_block()
        return result

    def parse_if(self) -> ast.If:
        result = ast.If()
        result.condition = self.parse_condition()
        result.if_block = self.parse_instruction_block()
        if self.peek(( TokenType.ELSE, )):
            self.accept(( TokenType.ELSE, ))
            result.else_block = self.parse_instruction_block()
        else:
            result.else_block = None
        return result

    def parse_condition(self) -> ast.Condition:
        result = ast.Condition()
        self.accept(( TokenType.ROUND_OPEN, ))
        result.first_operand = self.parse_assignable()
        result.operator = self.parse_logical_operator()
        result.second_operand = self.parse_assignable()
        self.accept(( TokenType.ROUND_CLOSE, ))
        return result

    def parse_log(self) -> ast.Log:
        result = ast.Log()
        result.value = self.parse_assignable()
        return result

    def parse_return(self) -> ast.Return:
        result = ast.Return()
        result.value = self.parse_assignable()
        return result

    def parse_logical_operator(self) -> TokenType:
        token = self.accept(( TokenType.LESS_THAN, TokenType.MORE_THAN, TokenType.LESS_OR_EQUAL, TokenType.MORE_OR_EQUAL, TokenType.EQUALS ))
        return token.t_type

    def parse_assignable(self) -> ast.Assignable:
        if self.peek(( TokenType.IDENTIFIER, )):
            identifier_token = self.accept(( TokenType.IDENTIFIER, ))
            if self.peek(( TokenType.ROUND_OPEN, )):
                return self.parse_function_call(identifier_token)
            else:
                return self.parse_expression(identifier_token)
        elif self.peek(( TokenType.STRING_LITERAL, )):
            return self.parse_string()
        else:
            return self.parse_expression()

    def parse_function_call(self, identifier: Token) -> ast.FunctionCall:
        result = ast.FunctionCall(identifier.t_value)
        result.arguments = self.parse_call_parameters()
        return result

    def parse_call_parameters(self) -> list:
        result = []
        self.accept(( TokenType.ROUND_OPEN, ))
        while not self.peek(( TokenType.ROUND_CLOSE, )):
            parameter = self.parse_assignable()
            result.append(parameter)
            if self.peek(( TokenType.COMMA, )):
                self.accept(( TokenType.COMMA, ))
        self.accept(( TokenType.ROUND_CLOSE, ))
        return result

    def parse_expression(self, token: Token = None) -> ast.Expression:
        result = ast.Expression()
        result.add_operand(self.parse_multiplicative_expression(token))
        while ( self.peek(( TokenType.PLUS, TokenType.MINUS )) ):
            op_token = self.accept(( TokenType.PLUS, TokenType.MINUS ))
            result.add_operator(op_token.t_type)
            result.add_operand(self.parse_multiplicative_expression())
        return result

    def parse_multiplicative_expression(self, token: Token = None) -> ast.Expression:
        result = ast.Expression()
        result.add_operand(self.parse_primary_expression(token))
        while ( self.peek(( TokenType.ASTERISK, TokenType.SLASH )) ):
            op_token = self.accept(( TokenType.ASTERISK, TokenType.SLASH ))
            result.add_operator(op_token.t_type)
            result.add_operand(self.parse_primary_expression())
        return result

    def parse_primary_expression(self, token: Token = None) -> ast.Expression:
        if token is not None:
            return self.parse_variable(token)
        elif self.peek(( TokenType.ROUND_OPEN, )):
            self.accept(( TokenType.ROUND_OPEN, ))
            result = self.parse_expression()
            self.accept(( TokenType.ROUND_CLOSE, ))
            return result
        elif self.peek(( TokenType.IDENTIFIER, )):
            t = self.accept(( TokenType.IDENTIFIER, ))
            if self.peek(( TokenType.ROUND_OPEN, )):
                return self.parse_function_call(t)
            return self.parse_variable(t)
        elif self.peek(( TokenType.CARET, )):
            return self.parse_dice_roll()
        elif self.peek(( TokenType.NUMBER_LITERAL, )):
            return self.parse_number()
        elif self.peek(( TokenType.DICE_LITERAL, )):
            return self.parse_dice()

    def parse_literal(self) -> ast.Literal:
        if self.peek(( TokenType.NUMBER_LITERAL, )):
            return self.parse_number()
        elif self.peek(( TokenType.STRING_LITERAL, )):
            return self.parse_string()
        elif self.peek(( TokenType.DICE_LITERAL, )):
            return self.parse_dice()

    def parse_number(self) -> ast.Number:
        number_token = self.accept(( TokenType.NUMBER_LITERAL, ))
        return ast.Number(number_token.t_value)
    
    def parse_string(self) -> ast.String:
        string_token = self.accept(( TokenType.STRING_LITERAL, ))
        return ast.String(string_token.t_value)

    def parse_dice(self) -> ast.Dice:
        dice_token = self.accept(( TokenType.DICE_LITERAL, ))
        return ast.Dice(dice_token.t_value)

    def parse_dice_roll(self) -> ast.DiceRoll:
        self.accept(( TokenType.CARET, ))
        if self.peek(( TokenType.DICE_LITERAL, )):
            return ast.DiceRoll(self.parse_dice())
        elif self.peek(( TokenType.IDENTIFIER, )):
            return ast.DiceRoll(self.parse_variable())

    def parse_variable(self, token: Token = None) -> ast.Variable:
        if token is None:
            token = self.accept(( TokenType.IDENTIFIER, ))
        return ast.Variable(token.t_value)
