import unittest
import io
import sys
sys.path.append('D:\Projects\dndlang-python')
from lexing.lexer import Lexer
from parsing.parser import Parser
from parsing import ast
from lexing.token import TokenType
from parsing.error_handling import UnexpectedTokenError
from interpreting.scope import Scope

class TestParserMethods(unittest.TestCase):

    def test_is_acceptable(self):
        test_lexer = Lexer(io.StringIO("item Gold { }"))
        test_parser = Parser(test_lexer)
        
        self.assertFalse(test_parser.is_acceptable( test_lexer.next_token(), ( TokenType.AND, ) ) )
        self.assertTrue(test_parser.is_acceptable( test_lexer.next_token(), ( TokenType.SLASH, TokenType.IDENTIFIER ) ) )

    def test_accept(self):
        test_lexer = Lexer(io.StringIO("item Gold { }"))
        test_parser = Parser(test_lexer)

        token = test_parser.accept(( TokenType.ITEM, ))
        self.assertEqual(token.t_type, TokenType.ITEM)

    def test_peek(self):
        test_lexer = Lexer(io.StringIO("item Gold { }"))
        test_parser = Parser(test_lexer)

        for i in range(0, 10):
            self.assertTrue(test_parser.peek(( TokenType.ITEM, )))
        token = test_parser.accept(( TokenType.ITEM, ))
        self.assertEqual(token.t_type, TokenType.ITEM)
        self.assertFalse(test_parser.peek(( TokenType.ITEM, )))
        self.assertTrue(test_parser.peek(( TokenType.IDENTIFIER, )))

    def test_parse_empty_item(self):
        test_lexer = Lexer(io.StringIO("item Gold { }"))
        test_parser = Parser(test_lexer)

        test_ast = test_parser.parse()

        self.assertEqual(len(test_ast.templates), 1)
        self.assertIsInstance(test_ast.templates[0], ast.Item)
        with self.assertRaises(AttributeError):
            test_ast.templates[0].desc
        with self.assertRaises(AttributeError):
            test_ast.templates[0].value

    def test_parse_item(self):
        test_lexer = Lexer(io.StringIO("item Gold { desc: \"Currency\" value: 1 }"))
        test_parser = Parser(test_lexer)

        test_ast = test_parser.parse()

        self.assertEqual(len(test_ast.templates), 1)
        self.assertIsInstance(test_ast.templates[0], ast.Item)
        self.assertEqual(test_ast.templates[0].name, "Gold")
        self.assertEqual(test_ast.templates[0].desc.value, "Currency")
        self.assertEqual(test_ast.templates[0].value.value, 1)

    def test_parse_character(self):
        test_lexer = Lexer(io.StringIO("character Paladin { level: 1 exp: 2 health: 10 attack: 2 defence: 0 equipped: HolySword inventory: Gold/5 & Shield }"))
        test_parser = Parser(test_lexer)

        test_ast = test_parser.parse()

        self.assertEqual(len(test_ast.templates), 1)
        self.assertIsInstance(test_ast.templates[0], ast.Character)
        self.assertEqual(test_ast.templates[0].name, "Paladin")
        self.assertEqual(test_ast.templates[0].level.value, 1)
        self.assertEqual(test_ast.templates[0].health.value, 10)
        self.assertEqual(test_ast.templates[0].equipped[0][0], "HolySword")
        self.assertEqual(test_ast.templates[0].equipped[0][1], 1)
        self.assertEqual(test_ast.templates[0].inventory[0][0], "Gold")
        self.assertEqual(test_ast.templates[0].inventory[0][1], 5)
        self.assertEqual(test_ast.templates[0].inventory[1][0], "Shield")

    def test_unit_parse_declaration(self):
        test_lexer = Lexer(io.StringIO("Knight John;"))
        test_parser = Parser(test_lexer)

        st = test_parser.parse_statement()

    def test_parse_declaration(self):
        test_lexer = Lexer(io.StringIO("Knight John;"))
        test_parser = Parser(test_lexer)

        test_ast = test_parser.parse()

        self.assertEqual(len(test_ast.instructions), 1)

    def test_parse_function_definition(self):
        test_lexer = Lexer(io.StringIO("function add(a, b) { return a + b; }"))
        test_parser = Parser(test_lexer)

        test_ast = test_parser.parse()

        self.assertEqual(len(test_ast.functions), 1)
        self.assertIsInstance(test_ast.functions[0], ast.FunctionDefinition)
        self.assertEqual(test_ast.functions[0].parameters[0].name, 'a')
        self.assertEqual(test_ast.functions[0].parameters[1].name, 'b')
        self.assertIsInstance(test_ast.functions[0].block.instructions[0], ast.Instruction)
        self.assertIsInstance(test_ast.functions[0].block.instructions[0], ast.Return)

    def test_parse_instruction_return(self):
        test_lexer = Lexer(io.StringIO("return 2;"))
        test_parser = Parser(test_lexer)

        test_return = test_parser.parse_instruction()

    def test_parse_while(self):
        test_lexer = Lexer(io.StringIO("while (i < 5) { Stefan >> Robert; }"))
        test_parser = Parser(test_lexer)

        test_ast = test_parser.parse()
        self.assertIsInstance(test_ast.instructions[0], ast.Instruction)
        self.assertIsInstance(test_ast.instructions[0], ast.While)
        
    def test_parse_if_in_while(self):
        test_lexer = Lexer(io.StringIO("while (i < 5) { if (i < 5) { i = i + 1; } else { } i = i + 1; }"))
        test_parser = Parser(test_lexer)

        test_ast = test_parser.parse()

        self.assertIsInstance(test_ast.instructions[0], ast.While)
        self.assertIsInstance(test_ast.instructions[0].block.instructions[0], ast.If)

    def test_parse_expression(self):
        test_input = "Number i; i = 2 + 2 / (2 * 2) + 1;"
        test_lexer = Lexer(io.StringIO(test_input))
        test_parser = Parser(test_lexer)

        test_ast = test_parser.parse()
        test_scope = Scope()

        self.assertEqual(test_ast.instructions[1].rhs.evaluate(test_scope), 3.5)

if __name__ == '__main__':
    unittest.main()
