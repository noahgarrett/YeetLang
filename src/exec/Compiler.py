from models.AST import Program, Node, Expression, Statement
from models.AST import LetStatement, ExpressionStatement, BlockStatement, ReturnStatement, FunctionStatement
from models.AST import InfixExpression, PrefixExpression, CallExpression
from models.AST import IntegerLiteral, IdentifierLiteral, FloatLiteral, StringLiteral, BooleanLiteral, FunctionLiteral

from llvmlite import ir



class Compiler:
    def __init__(self) -> None:
        self.type_map: dict = {
            'bool': ir.IntType(1),
            'int': ir.IntType(32),
            'float': ir.FloatType(),
            'double': ir.DoubleType(),
            'void': ir.VoidType(),
            'str': ir.ArrayType(ir.IntType(8), 1)  # String = array of chars (int8)
        }

        # Initializing the main module
        self.module: ir.Module = ir.Module('main')

        # Keeping track of defined variables
        self.variables: dict[str, tuple] = {}

        # Defining a builtin functions
        self.__initialize_builtins()

        # Current Builder
        self.builder: ir.IRBuilder = ir.IRBuilder()

    def compile(self, node: Node) -> None:
        match node.type():
            case "Program":
                self.__visit_program(node)
            
            # Statements
            case "LetStatement":
                self.__visit_let_statement(node)
            case "ExpressionStatement":
                self.__visit_expression_statement(node)
            case "BlockStatement":
                self.__visit_block_statement(node)
            case "ReturnStatement":
                self.__visit_return_statement(node)
            case "FunctionStatement":
                self.__visit_function_statement(node)

            # Expressions
            case "InfixExpression":
                self.__visit_infix_expression(node)
            case "CallExpression":
                self.__visit_call_expression(node)

    def __initialize_builtins(self) -> ir.Function:
        def __init_print() -> ir.Function:
            fnty: ir.FunctionType = ir.FunctionType(
                self.type_map['int'],
                [ir.IntType(8).as_pointer()],
                var_arg=True
            )
            return ir.Function(self.module, fnty, 'printf')
        
        self.variables['printf'] = (__init_print(), ir.IntType(32))
    
    # region Visit Methods
    def __visit_program(self, node: Program) -> None:
        # Compile the body of the function / program
        for stmt in node.statements:
            self.compile(stmt)

    # Statements
    def __visit_let_statement(self, node: LetStatement) -> None:
        name: str = node.name.value
        value: Expression = node.value

        value, Type = self.__resolve_value(node=value)

        if not self.variables.__contains__(name):
            # Creating a pointer for the type 'Type' : ir.Type
            ptr = self.builder.alloca(Type)

            # Storing the value to the pointer
            self.builder.store(value, ptr)

            # Adding the name and its pointer to the variables map
            self.variables[name] = ptr, Type
        else:
            ptr, _ = self.variables[name]
            self.builder.store(value, ptr)
    
    def __visit_expression_statement(self, node: ExpressionStatement) -> None:
        self.compile(node.expr)

    def __visit_block_statement(self, node: BlockStatement) -> None:
        for stmt in node.statements:
            self.compile(stmt)

    def __visit_return_statement(self, node: ReturnStatement) -> None:
        value = node.return_value
        value, Type = self.__resolve_value(value)
        self.builder.ret(value)

    def __visit_function_statement(self, node: FunctionStatement) -> None:
        name: str = node.name.value
        body: BlockStatement = node.body
        params: list[IdentifierLiteral] = node.parameters

        # Keep track of the names of each parameter
        param_names: list[str] = [p.value for p in params]

        # Keep track of the types for each parameter
        param_types: list[ir.Type] = [self.type_map[type(p.value).__name__] for p in params]

        # TODO: Function's return type (make better)
        return_type: ir.Type = self.type_map['void']
        for stmt in body.statements:
            if stmt.type() == 'ReturnStatement':
                return_type = self.type_map[type(stmt.return_value.value).__name__]
        
        # Defining the function's (return_type, params_type)
        fnty = ir.FunctionType(return_type, param_types)
        func = ir.Function(self.module, fnty, name=name)

        # Define the function's block
        block = func.append_basic_block(f'{name}_entry')

        previous_builder = self.builder

        # Current builder
        self.builder = ir.IRBuilder(block)

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

    # Expressions
    def __visit_infix_expression(self, node: InfixExpression) -> tuple:
        operator: str = node.operator
        left_value, left_type = self.__resolve_value(node.left_node)
        right_value, right_type = self.__resolve_value(node.right_node)

        value = None
        Type = None
        if isinstance(right_type, ir.FloatType) and isinstance(left_type, ir.FloatType):
            Type = ir.FloatType()
            match operator:
                case '+':
                    value = self.builder.fadd(left_value, right_value)
                case '-':
                    value = self.builder.fsub(left_value, right_value)
                case '*':
                    value = self.builder.fmul(left_value, right_value)
                case '/':
                    value = self.builder.fdiv(left_value, right_value)
        elif isinstance(right_type, ir.IntType) and isinstance(left_type, ir.IntType):
            Type = ir.IntType(32)
            match operator:
                case '+':
                    value = self.builder.add(left_value, right_value)
                case '-':
                    value = self.builder.sub(left_value, right_value)
                case '*':
                    value = self.builder.mul(left_value, right_value)
                case '/':
                    value = self.builder.sdiv(left_value, right_value)
        
        return value, Type
    
    def __visit_call_expression(self, node: CallExpression) -> tuple:
        name: str = node.function.value
        params: list[Expression] = node.arguments

        args = []
        types = []
        if params[0]:
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
    def __resolve_value(self, node: Expression) -> tuple[ir.Value, ir.Type]:
        """ Resolves a value and returns a tuple (ir_value, ir_type) """
        match node.type():
            # Literal Values
            case "IntegerLiteral":
                node: IntegerLiteral = node
                value, Type = node.value, self.type_map['int']
                return ir.Constant(Type, value), Type
            case "FloatLiteral":
                node: FloatLiteral = node
                value, Type = node.value, self.type_map['float']
                return ir.Constant(Type, value), Type
            case "StringLiteral":
                node: StringLiteral = node
                string, Type = self.__convert_string(node.value)
                return string, Type
            case "IdentifierLiteral":
                node: IdentifierLiteral = node
                ptr, Type = self.variables[node.value]
                return self.builder.load(ptr), Type
            
            # Expression Values
            case "InfixExpression":
                return self.__visit_infix_expression(node)


    def __convert_string(self, string: str) -> tuple[ir.Constant, ir.ArrayType]:
        """ Strings are converted into an array of characters """
        # string = string[1:-1]
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
