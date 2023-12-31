from models.AST import Program, Node, Expression, Statement
from models.AST import LetStatement
from models.AST import IntegerLiteral, IdentifierLiteral

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

        # Defining a builtin functions
        fnty: ir.FunctionType = ir.FunctionType(
            self.type_map['int'],
            [ir.IntType(8).as_pointer()],
            var_arg=True
        )
        func: ir.Function = ir.Function(self.module, fnty, 'print')

        # Keeping track of defined variables
        self.variables: dict[str, tuple] = {
            'print': (func, ir.IntType(32))
        }

        # Current Builder
        self.builder: ir.IRBuilder = ir.IRBuilder()

    def compile(self, node: Node) -> None:
        match node.type():
            case "Program":
                self.__visit_program(node)
            
            # Statements
            case "LetStatement":
                self.__visit_let_statement(node)
    
    # region Visit Methods
    def __visit_program(self, node: Program) -> None:
        # Create a fake main function so it does not need to be defined in the source code
        name: str = 'main'
        body: list[Statement] = node.statements
        params: list = []

        return_type = self.type_map['int']

        # Defining the function
        fnty: ir.FunctionType = ir.FunctionType(
            return_type=return_type,
            args=[]
        )
        func: ir.Function = ir.Function(self.module, fnty, name=name)

        # Define the function's block
        block: ir.Block = func.append_basic_block(f'{name}_entry')

        # Save the previous builder
        previous_builder: ir.IRBuilder = self.builder

        # Set the new current builder for the main function's scope
        self.builder = ir.IRBuilder(block=block)

        # Add the main function to variables
        self.variables[name] = func, return_type

        # Compile the body of the function / program
        for stmt in body:
            self.compile(stmt)

        # Return the builder back to normal
        self.builder = previous_builder

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
    # endregion
        
    # region Helper Methods
    def __resolve_value(self, node: Expression) -> tuple[ir.Value, ir.Type]:
        """ Resolves a value and returns a tuple (ir_value, ir_type) """
        match node.type():
            case "IntegerLiteral":
                node: IntegerLiteral = node
                value, Type = node.value, self.type_map['int']
                return ir.Constant(Type, value), Type
    # endregion
