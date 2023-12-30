from exec.Lexer import Lexer
from exec.Parser import Parser

from models.AST import Program

from utils import ast_to_json

if __name__ == '__main__':
    with open("./debug/test.yeet", "r") as f:
        code: str = f.read()

    l: Lexer = Lexer(source=code)

    p: Parser = Parser(lexer=l)

    program: Program = p.parse_program()
    if len(p.errors) > 0:
        for err in p.errors:
            print(err)
        exit(1)
    
    ast_to_json(program=program)
