import unittest
import io
import sys
sys.path.append('D:\Projects\dndlang-python')
from lexing.lexer import Lexer
from lexing.token import TokenType

class TestLexerMethods(unittest.TestCase):

    def test_token_type_recognition(self): 
        test_lexer = Lexer(io.StringIO("item character health attack defence level reqexp exp\n" +
                                        "equipped inventory reward desc value while if else\n" +
                                        "function return { } ( ) + - * / = += *= ; . : , & ^ < >\n" +
                                        "<= >= == >> ? blah 3125 \"Some string\" 5d47 %"))
        for t in TokenType:
            self.assertEqual(test_lexer.next_token().t_type, t)

    def test_token_value(self):
        test_lexer = Lexer(io.StringIO("2D4 547 some_identifier \"Test123\""))
        self.assertEqual(test_lexer.next_token().t_value, '2d4')
        self.assertEqual(test_lexer.next_token().t_value, '547')
        self.assertEqual(test_lexer.next_token().t_value, 'some_identifier')
        self.assertEqual(test_lexer.next_token().t_value, 'Test123')

if __name__ == '__main__':
    unittest.main()
