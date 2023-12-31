from exec.Lexer import Lexer
from exec.Parser import Parser
from exec.Compiler import Compiler

from models.AST import Program

from utils import ast_to_json

from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float

DEBUG: bool = False

if __name__ == '__main__':
    # with open("./debug/test.yeet", "r") as f:
    #     code: str = f.read()
    code: str = """
    let main = fn(c, d) {
        return 1;
    }
    """

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

    # Output Steps
    module: ir.Module = c.module
    module.triple = llvm.get_default_triple()

    if DEBUG:
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

    result = cfunc()
    print(f'Program returned: {result}')
