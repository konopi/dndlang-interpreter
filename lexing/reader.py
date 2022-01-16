from io import TextIOWrapper
import sys
from typing import NamedTuple
from recordtype import recordtype

class Reader:
    def __init__(self, io: TextIOWrapper) -> None:
        Position = recordtype('Position', 'line_no char_no', default = 0)
        self.position = Position(1, 0)
        self.io = io

    def next_char(self) -> str:
        # returns empty string if end of file was reached
        c = self.io.read(1)
        if (c == '\n'):
            self.position.line_no += 1
            self.position.char_no = 0
        else:
            self.position.char_no += 1
        return c

    def peek(self) -> str:
        # returns empty string if end of file was reached
        c = self.io.read(1)
        self.io.seek(self.io.tell() - 1)
        return c
