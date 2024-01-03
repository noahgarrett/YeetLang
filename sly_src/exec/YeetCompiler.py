from llvmlite import ir

from typing import NamedTuple

from models.YeetAST import Program, FunctionParam
from models.YeetAST import FunctionStatement, ReturnStatement, AssignStatement, CallStatement, IfStatement
from models.YeetAST import WhileStatement, ForStatement, BreakStatement, ContinueStatement
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

        # Keeps track of break points
        self.breakpoints = []

        # Keeps track of continue points
        self.continues = []

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
            # Statements
            if isinstance(node, FunctionStatement):
                self.__visit_function_statement(node)
            elif isinstance(node, AssignStatement):
                self.__visit_assign_statement(node)
            elif isinstance(node, ReturnStatement):
                self.__visit_return_statement(node)
            elif isinstance(node, CallStatement):
                self.__visit_call_statement(node)
            elif isinstance(node, IfStatement):
                self.__visit_if_statement(node)
            elif isinstance(node, WhileStatement):
                self.__visit_while_statement(node)
            elif isinstance(node, ForStatement):
                self.__visit_for_statement(node)
            elif isinstance(node, BreakStatement):
                self.__visit_break_statement(node)
            elif isinstance(node, ContinueStatement):
                self.__visit_continue_statement(node)

            # Expressions
                
            # Literals

    # region Visit Methods
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

    def __visit_call_statement(self, node: CallStatement) -> tuple[ir.Value, ir.Type]:
        name: str = node.name
        params: list = [p for p in node.params if p is not None]

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
    
    def __visit_if_statement(self, node: IfStatement) -> None:
        condition = node.condition
        true_body = node.true_body
        else_body = node.else_body

        condition_value, Type = self.__resolve_value(condition)

        # If there is not an else block
        if else_body == []:
            with self.builder.if_then(condition_value):
                self.compile(true_body)
        else:
            with self.builder.if_else(condition_value) as (true, otherwise):
                with true:
                    self.compile(true_body)
                
                with otherwise:
                    self.compile(else_body)

    def __visit_while_statement(self, node: WhileStatement) -> None:
        condition = node.condition
        true_body = node.true_body

        condition_value, _ = self.__resolve_value(condition)

        # Entry block that runs when the condtion is true
        while_loop_entry = self.builder.append_basic_block(f"while_loop_entry_{self.inc_counter()}")

        # If the condition is not true, it runs from this block
        while_loop_otherwise = self.builder.append_basic_block(f"while_loop_otherwise_{self.counter}")

        # Create the condition branch
        self.builder.cbranch(condition_value, while_loop_entry, while_loop_otherwise)

        # Setting the builder position at the start
        self.builder.position_at_start(while_loop_entry)

        # Adding the breakpoint if a break statement is ran | Adding continue point
        self.breakpoints.append(while_loop_otherwise)
        self.continues.append(while_loop_entry)

        self.compile(true_body)

        condition_value, _ = self.__resolve_value(condition)

        self.builder.cbranch(condition_value, while_loop_entry, while_loop_otherwise)
        self.builder.position_at_start(while_loop_otherwise)

        # Removing the added breakpoint
        self.breakpoints.pop()
        self.continues.pop()

    def __visit_for_statement(self, node: ForStatement) -> None:
        assign_statement: AssignStatement = node.assign_statement
        condition = node.condition
        step = node.step
        true_body = node.true_body

        # Compile the for loop variable
        self.compile([assign_statement])

        for_loop_entry = self.builder.append_basic_block(f"for_loop_entry_{self.inc_counter()}")
        for_loop_otherwise = self.builder.append_basic_block(f"for_loop_otherwise_{self.counter}")

        self.builder.branch(for_loop_entry)
        self.builder.position_at_start(for_loop_entry)

        # Adding the breakpoint if a break statement is ran | Adding continue point
        self.breakpoints.append(for_loop_otherwise)
        self.continues.append(for_loop_entry)

        # Compile the loop body
        self.compile(true_body)

        self.compile([step])

        condition_value, _ = self.__resolve_value(condition)

        self.builder.cbranch(condition_value, for_loop_entry, for_loop_otherwise)

        self.builder.position_at_start(for_loop_otherwise)

        self.breakpoints.pop()
        self.continues.pop()

    def __visit_break_statement(self, node: BreakStatement) -> None:
        self.builder.branch(self.breakpoints[-1])

    def __visit_continue_statement(self, node: ContinueStatement) -> None:
        self.builder.branch(self.continues[-1])

    def __visit_binary_expression(self, node: BinaryExpression) -> tuple[ir.Value, ir.Type]:
        operator: str = node.operator
        lhs, lhs_type = self.__resolve_value(node.left_side)
        rhs, rhs_type = self.__resolve_value(node.right_side)

        value, Type = None, None

        # float `op` float
        if isinstance(rhs_type, ir.FloatType) and isinstance(lhs_type, ir.FloatType):
            Type = ir.FloatType()
            match operator:
                case "+":
                    value = self.builder.fadd(lhs, rhs)
                case "-":
                    value = self.builder.fsub(lhs, rhs)
                case "*":
                    value = self.builder.fmul(lhs, rhs)
                case "/":
                    value = self.builder.fdiv(lhs, rhs)
                case "%":
                    value = self.builder.frem(lhs, rhs)
                case "<":
                    value = self.builder.fcmp_ordered('<', lhs, rhs)
                    Type = ir.IntType(1)
                case "<=":
                    value = self.builder.fcmp_ordered('<=', lhs, rhs)
                    Type = ir.IntType(1)
                case ">":
                    value = self.builder.fcmp_ordered('>', lhs, rhs)
                    Type = ir.IntType(1)
                case ">=":
                    value = self.builder.fcmp_ordered('>=', lhs, rhs)
                    Type = ir.IntType(1)
                case "!=":
                    value = self.builder.fcmp_ordered('!=', lhs, rhs)
                    Type = ir.IntType(1)
                case "==":
                    value = self.builder.fcmp_ordered('==', lhs, rhs)
                    Type = ir.IntType(1)

        # int `op` int
        elif isinstance(rhs_type, ir.IntType) and isinstance(lhs_type, ir.IntType):
            Type = ir.IntType(32)
            match operator:
                case "+":
                    value = self.builder.add(lhs, rhs)
                case "-":
                    value = self.builder.sub(lhs, rhs)
                case "*":
                    value = self.builder.mul(lhs, rhs)
                case "/":
                    value = self.builder.sdiv(lhs, rhs)
                case "%":
                    value = self.builder.srem(lhs, rhs)
                case "<":
                    value = self.builder.icmp_signed('<', lhs, rhs)
                    Type = ir.IntType(1)
                case "<=":
                    value = self.builder.icmp_signed('<=', lhs, rhs)
                    Type = ir.IntType(1)
                case ">":
                    value = self.builder.icmp_signed('>', lhs, rhs)
                    Type = ir.IntType(1)
                case ">=":
                    value = self.builder.icmp_signed('>=', lhs, rhs)
                    Type = ir.IntType(1)
                case "!=":
                    value = self.builder.icmp_signed('!=', lhs, rhs)
                    Type = ir.IntType(1)
                case "==":
                    value = self.builder.icmp_signed('==', lhs, rhs)
                    Type = ir.IntType(1)

        return value, Type
    # endregion 
            
    # region Helper Methods
    def __resolve_value(self, node: NamedTuple) -> tuple[ir.Value, ir.Type]:
        # Literals
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
        
        # Expressions
        elif isinstance(node, BinaryExpression):
            return self.__visit_binary_expression(node)
        
        # Statements
        elif isinstance(node, CallStatement):
            return self.__visit_call_statement(node)

        
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
    