from llvmlite import ir

from models.YeetAST import Program

class YeetCompiler:
    def __init__(self) -> None:
        self.type_map: dict[str, ir.Type] = {
            'bool': ir.IntType(1),
            'int': ir.IntType(32),
            'float': ir.FloatType(),
            'double': ir.DoubleType(),
            'void': ir.VoidType(),
            'str': ir.ArrayType(ir.IntType(8), 1)  # TODO: FIGURE OUT DAMN STRINGS
        }

        self.module: ir.Module = ir.Module("main")

        # Define the SymbolTable
        self.variables: dict = {}

        # Define builtin functions
        self.__initialize_builtins()

    def __initialize_builtins(self) -> None:
        def init_print() -> ir.Function:
            fnty = ir.FunctionType(self.type_map['int'], [ir.IntType(8).as_pointer()], var_arg=True)
            return ir.Function(self.module, fnty, 'printf')
        
        self.variables['printf'] = (init_print(), ir.IntType(32))

    def compile(self, program: Program) -> None:
        pass