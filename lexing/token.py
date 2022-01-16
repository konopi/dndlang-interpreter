from enum import Enum, auto

class TokenType(Enum):
    # keywords (templates, general)
    ITEM = auto()
    CHARACTER = auto()
    HEALTH = auto()
    ATTACK = auto()
    DEFENCE = auto()
    # keywords (character)
    LEVEL = auto()
    REQEXP = auto()
    EXP = auto()
    EQUIPPED = auto()
    INVENTORY = auto()
    REWARD = auto()
    # keywords (item)
    DESC = auto()
    VALUE = auto()
    # keywords (instructions)
    WHILE = auto()
    IF = auto()
    ELSE = auto()
    FUNCTION = auto()
    RETURN = auto()

    # special characters
    CURLY_OPEN = auto()     # {
    CURLY_CLOSE = auto()    # }
    ROUND_OPEN = auto()     # (
    ROUND_CLOSE = auto()    # )
    PLUS = auto()           # +
    MINUS = auto()          # -
    ASTERISK = auto()       # *
    SLASH = auto()          # /
    ASSIGN = auto()         # =
    INCREASES_BY = auto()   # +=
    MULTIPLIES_BY = auto()  # *=
    SEMICOLON = auto()      # ;
    DOT = auto()            # .
    COLON = auto()          # :
    COMMA = auto()          # ,
    AND = auto()            # &
    CARET = auto()          # ^
    LESS_THAN = auto()      # <
    MORE_THAN = auto()      # >
    LESS_OR_EQUAL = auto()  # <=
    MORE_OR_EQUAL = auto()  # >=
    EQUALS = auto()         # ==
    ATTACK_MOVE = auto()    # >>
    QUESTION_MARK = auto()  # ?

    # identifier, literals
    IDENTIFIER = auto()
    NUMBER_LITERAL = auto()
    STRING_LITERAL = auto()
    DICE_LITERAL = auto()

    UNKNOWN = auto()
    END_OF_FILE = auto()

class Token:
    def __init__(self, token_value = '', token_type = TokenType.UNKNOWN):
        self.t_value: str = token_value
        self.t_type: TokenType = token_type
    def __repr__(self) -> str:
        return '<Token t_value:%s t_type:%s>' % (self.t_value, self.t_type)
    def __str__(self) -> str:
        return "[Value: %s\tType: %s]" % (self.t_value, self.t_type)
