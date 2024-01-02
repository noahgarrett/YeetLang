from exec.YeetLexer import YeetLexer
from exec.YeetParser import YeetParser
from sly.lex import Token
import pprint

DEBUG_LEXER: bool = False
DEBUG_PARSER: bool = True

if __name__ == '__main__':
    with open("./debug/test.yeet", "r") as f:
        code: str = f.read()

    # Lexer Pass
    l: YeetLexer = YeetLexer()
    tokens = l.tokenize(code)

    if DEBUG_LEXER:
        t_copy = list(tokens)
        for t in t_copy:
            print(t)

    # Parser Pass
    p: YeetParser = YeetParser()
    p.parse(tokens)

    if DEBUG_PARSER:
        print(pprint.pformat(p.program.statements))

    # Type Checking Pass

    # Compiler Pass

    # Execution Pass
