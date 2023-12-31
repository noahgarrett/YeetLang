from exec.Lexer import Lexer
from exec.Parser import Parser
from exec.Compiler import Compiler

from models.AST import Program

from utils import ast_to_json

DEBUG: bool = True

if __name__ == '__main__':
    with open("./debug/test.yeet", "r") as f:
        code: str = f.read()
    # code: str = "let a = 45 + 5;"

    l: Lexer = Lexer(source=code)

    p: Parser = Parser(lexer=l)

    program: Program = p.parse_program()
    if len(p.errors) > 0:
        for err in p.errors:
            print(err)
        exit(1)
    
    if DEBUG:
        ast_to_json(program=program)

    c: Compiler = Compiler()
    c.compile(node=program)

    if DEBUG:
        # Print the IR to debug file
        with open("./debug/test-ir.ll", "w") as f:
            f.write(str(c.module))
