from typing import NamedTuple, TypedDict, List, Any

class ProgramStatements(TypedDict):
    body: List

class Program(NamedTuple):
    name: str
    statements: ProgramStatements

# region Statements
class FunctionStatement(NamedTuple):
    name: str
    return_type: str
    body: Any
    params: List

class ReturnStatement(NamedTuple):
    return_value: Any

class AssignStatement(NamedTuple):
    name: str
    value: Any

class CallStatement(NamedTuple):
    name: str
    params: List

class IfStatement(NamedTuple):
    condition: Any
    true_body: Any
    else_body: Any

class WhileStatement(NamedTuple):
    condition: Any
    true_body: Any

class ForStatement(NamedTuple):
    assign_statement: AssignStatement
    condition: Any
    step: Any
    true_body: Any

class BreakStatement(NamedTuple):
    temp: Any

class ContinueStatement(NamedTuple):
    temp: Any
# endregion
        
# region Expressions
class BinaryExpression(NamedTuple):
    left_side: Any
    operator: str
    right_side: Any
# endregion
        
# region Literals
class IdentifierLiteral(NamedTuple):
    value: str

class IntegerLiteral(NamedTuple):
    value: int

class FloatLiteral(NamedTuple):
    value: float

class StringLiteral(NamedTuple):
    value: str
# endregion
    
# region Misc
class FunctionParam(NamedTuple):
    name: str
    type: str
# endregion