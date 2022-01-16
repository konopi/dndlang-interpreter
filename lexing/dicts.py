from .token import TokenType

KEYWORDS = {
    'item': TokenType.ITEM,
    'character': TokenType.CHARACTER,

    'level': TokenType.LEVEL,
    'reqexp': TokenType.REQEXP,
    'exp': TokenType.EXP,
    'health': TokenType.HEALTH,
    'attack': TokenType.ATTACK,
    'defence': TokenType.DEFENCE,
    'equipped': TokenType.EQUIPPED,
    'inventory': TokenType.INVENTORY,
    'reward': TokenType.REWARD,

    'desc': TokenType.DESC,
    'value': TokenType.VALUE,

    'while': TokenType.WHILE,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'function': TokenType.FUNCTION,
    'return': TokenType.RETURN
}

SINGLE_SPECIAL_CHARACTERS = {
    '{': TokenType.CURLY_OPEN,
    '}': TokenType.CURLY_CLOSE,
    '(': TokenType.ROUND_OPEN,
    ')': TokenType.ROUND_CLOSE,
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.ASTERISK,
    '/': TokenType.SLASH,
    '=': TokenType.ASSIGN,
    ';': TokenType.SEMICOLON,
    '.': TokenType.DOT,
    ':': TokenType.COLON,
    ',': TokenType.COMMA,
    '&': TokenType.AND,
    '^': TokenType.CARET,
    '?': TokenType.QUESTION_MARK
}
