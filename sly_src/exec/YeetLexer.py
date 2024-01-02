from sly import Lexer

def group(*choices): return '(' + '|'.join(choices) + ')'
def any(*choices): return group(*choices) + '*'
def maybe(*choices): return group(*choices) + '?'

Hexnumber = r'0[xX](?:_?[0-9a-fA-F])+'
Binnumber = r'0[bB](?:_?[01])+'
Octnumber = r'0[oO](?:_?[0-7])+'
Decnumber = r'(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Exponent = r'[eE][-+]?[0-9](?:_?[0-9])*'
Pointfloat = group(r'[0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?',
                   r'\.[0-9](?:_?[0-9])*') + maybe(Exponent)
Expfloat = r'[0-9](?:_?[0-9])*' + Exponent

class YeetLexer(Lexer):
    tokens: set = {
        # Data Types
        IDENT,
        INT,
        FLOAT,
        STRING,

        # Arithmetic Operators
        PLUS,
        MINUS,
        ASTERISK,
        SLASH,
        POW,
        MODULUS,

        # Comparison Operators
        LT,
        LTE,
        GT,
        GTE,
        EQEQ,
        NOTEQ,

        # Assignment Operator
        EQ,

        # Symbols
        LPAREN,
        RPAREN,
        LBRACE,
        RBRACE,
        LBRACKET,
        RBRACKET,
        SEMICOLON,
        COMMA,
        
        # Type Declarations
        COLON,
        ARROW,

        # Keywords
        LET,
        IF,
        ELIF,
        ELSE,
        FN,
        RETURN,
        FOR,
        WHILE,
        BREAK,
        CONTINUE,
        AND,
        OR
    }

    literals: set = {',', ';'}

    FLOAT = group(Pointfloat, Expfloat)

    INT = group(
        Hexnumber,
        Binnumber,
        Octnumber,
        Decnumber
    )

    ignore = ' \t\r'
    @_(r'\n')
    def newline(self, t):
        self.lineno += 1

    # Keyword Declarations
    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENT['let'] = LET
    IDENT['if'] = IF
    IDENT['elif'] = ELIF
    IDENT['else'] = ELSE
    IDENT['fn'] = FN
    IDENT['return'] = RETURN
    IDENT['for'] = FOR
    IDENT['while'] = WHILE
    IDENT['break'] = BREAK
    IDENT['continue'] = CONTINUE
    IDENT['and'] = AND
    IDENT['or'] = OR

    # Other Token Definitions
    STRING = r'(\".*?\")|(\'.*?\')'
    GTE = r'>='
    GT = r'>'
    LTE = r'<='
    LT = r'<'
    NOTEQ = r'!='
    EQEQ = r'=='
    EQ = r'='
    LBRACE = r'\{'
    RBRACE = r'\}'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    PLUS = r'\+'
    ARROW = r'->'
    MINUS = r'-'
    ASTERISK = r'\*'
    SLASH = r'/'
    MODULUS = r'%'
    COLON = r':'
    COMMA = r','

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    def error(self, t):
        print(f'Illegal Character {t.value[0]}, in Line {self.lineno}, Column {self.index}')
        exit(1)