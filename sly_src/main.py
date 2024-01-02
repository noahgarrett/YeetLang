from exec.YeetLexer import YeetLexer
from exec.YeetParser import YeetParser
from exec.YeetCompiler import YeetCompiler
from sly.lex import Token
import pprint

import time
from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float

DEBUG_LEXER: bool = False
DEBUG_PARSER: bool = False
DEBUG_IR: bool = True

if __name__ == '__main__':
    # with open("./debug/test.yeet", "r") as f:
    #     code: str = f.read()

    code = """
    fn main() -> int {
        c = 4
        c = 7
        printf("apples %i", c)
        return c
    }
    """

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
    c: YeetCompiler = YeetCompiler()
    c.compile(p.program.statements['body'])

    # Execution Pass
    module: ir.Module = c.module
    module.triple = llvm.get_default_triple()

    if DEBUG_IR:
        # Print the IR to debug file
        with open("./debug/test-ir.ll", "w") as f:
            f.write(str(module))
    
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    try:
        llvm_ir_parsed = llvm.parse_assembly(str(module))
        llvm_ir_parsed.verify()
    except Exception as e:
        print(e)
        raise

    target_machine = llvm.Target.from_default_triple().create_target_machine()

    engine = llvm.create_mcjit_compiler(llvm_ir_parsed, target_machine)
    engine.finalize_object()

    # Run the function with the name 'main'. This is the entry point function of the entire program
    entry = engine.get_function_address('main')
    cfunc = CFUNCTYPE(c_int)(entry)

    st = time.time()

    result = cfunc()

    et = time.time()

    print(f'\n\nProgram returned: {result}\n=== Executed in {round((et - st) * 1000, 6)} ms. ===')

