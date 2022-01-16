class LexerError(Exception):
    pass

class DiceLiteralError(LexerError):
    '''Raised when the dice literal was incorrectly specified'''
    pass
class StringLiteralError(LexerError):
    '''Raised when the string literal was incorrectly specified'''
    pass
