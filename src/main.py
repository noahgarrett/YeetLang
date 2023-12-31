from exec.Lexer import Lexer
from exec.Parser import Parser
from exec.Compiler import Compiler

from models.AST import Program

from utils import ast_to_json

from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float
import time

DEBUG: bool = True

if __name__ == '__main__':
    # with open("./debug/mandel.yeet", "r") as f:
    #     code: str = f.read()
    code: str = """
bruh in_mandelbrot(xP, yP, n) {
    let x = 0.0;
    let y = 0.0;
    let xtemp = 0.0;

    while n > 0.0 {
        xtemp = (x * x) - (y * y) + xP;
        y = (2.0 * x * y) + yP;
        x = xtemp;
        n = n - 1.0;

        if x * x + y * y > 4.0 {
            return 0;
        }
    }

    return 1;
}

bruh mandel() {
    let xmin = -2.0;
    let xmax = 1.0;
    let ymin = -1.5;
    let ymax = 1.5;
    let width = 80.0;
    let height = 40.0;
    let threshold = 1000.0;

    let dx = (xmax - xmin) / width;
    let dy = (ymax - ymin) / height;

    let y = ymax;
    let x = 0.0;

    while y >= ymin {
        x = xmin;

        while x < xmax {
            if in_mandelbrot(x, y, threshold) == 1 {
                printf("*");
            } else {
                printf(".");
            }

            x = x + dx;
        }

        printf("\n");
        y = y - dy;
    }

    return 0;
}

bruh main() {
    return mandel();
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

    st = time.time()

    result = cfunc()

    et = time.time()

    print(f'\n\nProgram returned: {result}\n=== Executed in {round((et - st) * 1000, 6)} ms. ===')
