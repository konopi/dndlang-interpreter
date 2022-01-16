import unittest
import io
import sys
sys.path.append('D:\Projects\dndlang-python')
from lexing.reader import Reader

class TestReaderMethods(unittest.TestCase):

    def test_next_char_peek(self):
        test_reader = Reader(io.StringIO("afiudscb wbaiudbsa\n123456"))
        
        self.assertEqual(test_reader.next_char(), 'a')
        for i in range(0, 20):
            self.assertEqual(test_reader.peek(), 'f')
        self.assertEqual(test_reader.next_char(), 'f')
        
        test_string = ''
        while test_reader.position.line_no == 0:
            test_string += test_reader.next_char()
        self.assertEqual(test_string, "iudscb wbaiudbsa\n")
        self.assertEqual(test_reader.position.line_no, 1)
        self.assertEqual(test_reader.position.char_no, 0)


if __name__ == '__main__':
    unittest.main()
