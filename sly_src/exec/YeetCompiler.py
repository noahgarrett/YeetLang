from llvmlite import ir

from typing import NamedTuple

from models.YeetAST import Program, FunctionParam
from models.YeetAST import FunctionStatement, ReturnStatement, AssignStatement, CallStatement
from models.YeetAST import BinaryExpression
from models.YeetAST import IdentifierLiteral, IntegerLiteral, FloatLiteral, StringLiteral

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

        self.builder: ir.IRBuilder = ir.IRBuilder()

        # Random counter for entries
        self.counter = -1

    def inc_counter(self) -> int:
        self.counter += 1
        return self.counter

    def __initialize_builtins(self) -> None:
        def init_print() -> ir.Function:
            fnty = ir.FunctionType(self.type_map['int'], [ir.IntType(8).as_pointer()], var_arg=True)
            return ir.Function(self.module, fnty, 'printf')
        
        self.variables['printf'] = (init_print(), ir.IntType(32))

    def compile(self, ast: tuple) -> None:
        for node in ast:
            if isinstance(node, Program):
                self.__visit_program(node)

            # Statements
            elif isinstance(node, FunctionStatement):
                self.__visit_function_statement(node)
            elif isinstance(node, AssignStatement):
                self.__visit_assign_statement(node)
            elif isinstance(node, ReturnStatement):
                self.__visit_return_statement(node)
            elif isinstance(node, CallStatement):
                self.__visit_call_statement(node)

            # Expressions
                
            # Literals

    # region Visit Methods
    def __visit_program(self, node: Program) -> None:
        for stmt in node.statements['body']:
            self.compile(stmt)

    def __visit_function_statement(self, node: FunctionStatement) -> None:
        name: str = node.name
        body: list = node.body
        params: list[FunctionParam] = node.params

        # Keep track of the names for each parameter
        param_names: list[str] = [p.name for p in params if p is not None]

        # Keep track of the types for each parameter
        param_types: list[str] = [self.type_map[p.type] for p in params if p is not None]

        # Grab the function's declared return type
        return_type: ir.Type = self.type_map[node.return_type]

        # Define the function's IR
        fnty = ir.FunctionType(return_type, param_types)
        func = ir.Function(self.module, fnty, name=name)

        # Define the function's block
        block = func.append_basic_block(f'{name}_entry_block')

        previous_builder: ir.IRBuilder = self.builder

        # Current Builder
        self.builder = ir.IRBuilder(block=block)

        params_ptr = []

        # Storing the pointers of each param
        for i, typ in enumerate(param_types):
            ptr = self.builder.alloca(typ)
            self.builder.store(func.args[i], ptr)
            params_ptr.append(ptr)
        
        previous_variables = self.variables.copy()
        for i, x in enumerate(zip(param_types, param_names)):
            typ = param_types[i]
            ptr = params_ptr[i]

            # Add the function's parameter to the stored variables
            self.variables[x[1]] = ptr, typ
        
        # Adding the function to variables
        self.variables[name] = func, return_type

        # Compile the body of the function
        self.compile(body)

        # Removing the function's variables so it cannot be accessed by other functions
        self.variables = previous_variables
        self.variables[name] = func, return_type

        self.builder = previous_builder
    
    def __visit_assign_statement(self, node: AssignStatement) -> None:
        name: str = node.name
        value = node.value

        value, Type = self.__resolve_value(value)

        if not self.variables.__contains__(name):
            ptr = self.builder.alloca(Type)
            
            self.builder.store(value, ptr)

            self.variables[name] = ptr, Type
        else:
            ptr, _ = self.variables[name]
            self.builder.store(value, ptr)
    
    def __visit_return_statement(self, node: ReturnStatement) -> None:
        value = node.return_value
        value, Type = self.__resolve_value(value)
        self.builder.ret(value)

    def __visit_call_statement(self, node: CallStatement) -> None:
        name: str = node.name
        params: list = node.params

        args = []
        types = []
        if len(params) > 0:
            for x in params:
                p_val, p_type = self.__resolve_value(x)
                args.append(p_val)
                types.append(p_type)

        # See if we are calling a built-in function or an user-defined function
        match name:
            case 'printf':
                ret = self.builtin_printf(params=args, return_type=types[0])
                ret_type = self.type_map['int']
            case _:
                func, ret_type = self.variables[name]
                ret = self.builder.call(func, args)
        
        return ret, ret_type
    # endregion 
            
    # region Helper Methods
    def __resolve_value(self, node: NamedTuple) -> tuple[ir.Value, ir.Type]:
        if isinstance(node, IntegerLiteral):
            node: IntegerLiteral = node
            value, Type = node.value, self.type_map['int']
            return ir.Constant(Type, value), Type
        elif isinstance(node, FloatLiteral):
            node: FloatLiteral = node
            value, Type = node.value, self.type_map['float']
            return ir.Constant(Type, value), Type
        elif isinstance(node, IdentifierLiteral):
            node: IdentifierLiteral = node
            ptr, Type = self.variables[node.value]
            return self.builder.load(ptr), Type
        elif isinstance(node, StringLiteral):
            node: StringLiteral = node
            string, Type = self.__convert_string(node.value)
            return string, Type
        
    def __convert_string(self, string: str) -> tuple[ir.Constant, ir.ArrayType]:
        """ Strings are converted into an array of characters """
        string = string[1:-1]
        string = string.replace('\\n', '\n\0')
        n = len(string) + 1
        buf = bytearray((' ' * n).encode('ascii'))
        buf[-1] = 0
        buf[:-1] = string.encode('utf8')
        return ir.Constant(ir.ArrayType(ir.IntType(8), n), buf), ir.ArrayType(ir.IntType(8), n)
    # endregion
        
    # region Builtin Functions
    def builtin_printf(self, params: list, return_type: ir.Type) -> None:
        """ Basic C builtin printf """

        format = params[0]
        params = params[1:]
        zero = ir.Constant(ir.IntType(32),0)
        ptr = self.builder.alloca(return_type)
        self.builder.store(format,ptr)
        format = ptr
        format = self.builder.gep(format, [zero, zero])
        format = self.builder.bitcast(format, ir.IntType(8).as_pointer())
        func,_ = self.variables['printf']
        return self.builder.call(func,[format,*params])
    # endregion
    