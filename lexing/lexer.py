from . import reader, token, dicts, error_handling
import sys
from copy import deepcopy
from io import TextIOWrapper

class Lexer:
    def __init__(self, io: TextIOWrapper) -> None:
        self.reader = reader.Reader(io)

    def next_token(self) -> token.Token:
        try:
            c = self.next_non_whitespace_char()
            # end of file
            if c == '':
                return token.Token(token_type = token.TokenType.END_OF_FILE)
            elif c.isalpha() or c == '_':
                return self.get_keyword_or_identifier(c)
            elif c.isdecimal():
                return self.get_number_or_dice_literal(c)
            elif c == '"':
                return self.get_string_literal()
            else:
                return self.get_special_character(c)
        except error_handling.LexerError as e:
            print(e)
            sys.exit()

    def end(self):
        while c := self.next_non_whitespace_char() != '':
            pass

    def next_non_whitespace_char(self) -> str:
        c = self.reader.next_char()
        while c.isspace():
            c = self.reader.next_char()
        return c

    def get_keyword_or_identifier(self, c: str) -> token.Token:
        string = c
        pc = self.reader.peek()
        while pc.isalpha() or pc == '_':
            string += self.reader.next_char()
            pc = self.reader.peek()
        if string in dicts.KEYWORDS:
            # keyword
            return token.Token(token_type = dicts.KEYWORDS[string])
        else:
            # identifier
            return token.Token(token_value = string, token_type = token.TokenType.IDENTIFIER)

    def get_number_or_dice_literal(self, c: str) -> token.Token:
        first_decimal = c
        pc = self.reader.peek()
        while pc.isdecimal():
            first_decimal += self.reader.next_char()
            pc = self.reader.peek()
        if pc == 'd' or pc == 'D':
            self.reader.next_char()
            pc = self.reader.peek()
            if pc.isdecimal():
                second_decimal = self.reader.next_char()
                pc = self.reader.peek()
                while pc.isdecimal():
                    second_decimal += self.reader.next_char()
                    pc = self.reader.peek()
                return token.Token(token_value = first_decimal + 'd' + second_decimal, token_type = token.TokenType.DICE_LITERAL)
            else:
                raise error_handling.DiceLiteralError("DiceLiteralError: Dice literal without the amount of faces, line " \
                                                        + str(self.reader.position.line_no) + ", char " + str(self.reader.position.char_no))
        else:
            return token.Token(token_value = first_decimal, token_type = token.TokenType.NUMBER_LITERAL)

    def get_string_literal(self) -> token.Token:
        string_start = deepcopy(self.reader.position)
        string_value = ''
        pc = self.reader.peek()
        while pc != '"' and pc != '':
            string_value += self.reader.next_char()
            pc = self.reader.peek()
        if pc == '"':
            self.reader.next_char()
            return token.Token(token_value = string_value, token_type = token.TokenType.STRING_LITERAL)
        else:
            raise error_handling.StringLiteralError("StringLiteralError: String opening without closing, line " \
                                                    + str(string_start.line_no) + ", char " + str(string_start.char_no))

    def get_special_character(self, c: str) -> token.Token:
        if c == '+':
            if self.reader.peek() == '=':
                # +=
                self.reader.next_char()
                return token.Token(token_type = token.TokenType.INCREASES_BY)
            else:
                # +
                return token.Token(token_type = token.TokenType.PLUS)
        elif c == '*':
            if self.reader.peek() == '=':
                # *=
                self.reader.next_char()
                return token.Token(token_type = token.TokenType.MULTIPLIES_BY)
            else:
                # *
                return token.Token(token_type = token.TokenType.ASTERISK)
        elif c == '>':
            if self.reader.peek() == '>':
                # >>
                self.reader.next_char()
                return token.Token(token_type = token.TokenType.ATTACK_MOVE)
                
            elif self.reader.peek() == '=':
                # >=
                self.reader.next_char()
                return token.Token(token_type = token.TokenType.MORE_OR_EQUAL)
            else:
                # >
                return token.Token(token_type = token.TokenType.MORE_THAN)
        elif c == '<':
            if self.reader.peek() == '=':
                # <=
                self.reader.next_char()
                return token.Token(token_type = token.TokenType.LESS_OR_EQUAL)
            else:
                # <
                return token.Token(token_type = token.TokenType.LESS_THAN)
        elif c == '=':
            if self.reader.peek() == '=':
                # ==
                self.reader.next_char()
                return token.Token(token_type = token.TokenType.EQUALS)
            else:
                # =
                return token.Token(token_type = token.TokenType.ASSIGN)
        else:
            # other single special character
            if c in dicts.SINGLE_SPECIAL_CHARACTERS:
                return token.Token(token_type = dicts.SINGLE_SPECIAL_CHARACTERS[c])
            else:
                return token.Token(token_value = c, token_type = token.TokenType.UNKNOWN)

if __name__ == '__main__':
    from .token import TokenType

    fname = 'ex_code.adv'

    try:
        file = open(fname, 'r')
        lexer = Lexer(file)
        token = lexer.next_token()
        while token.t_type != TokenType.END_OF_FILE:
            print(token)
            token = lexer.next_token()
        print(token)
    except OSError:
        print("Could not open file: " + fname)
        sys.exit()
    finally:
        file.close()
