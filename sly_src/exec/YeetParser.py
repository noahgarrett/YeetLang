from sly import Parser
from exec.YeetLexer import YeetLexer

from models.YeetAST import Program
from models.YeetAST import ReturnStatement, FunctionStatement, AssignStatement, CallStatement
from models.YeetAST import BinaryExpression
from models.YeetAST import IdentifierLiteral, IntegerLiteral, FloatLiteral, StringLiteral
from models.YeetAST import FunctionParam

class YeetParser(Parser):
    tokens = YeetLexer.tokens

    precedence = (
        ('nonassoc', NOTEQ, LT, LTE, GT, GTE, EQEQ, AND, OR),
        ('left', PLUS, MINUS),
        ('left', ASTERISK, SLASH)
    )

    def __init__(self) -> None:
        self.program: Program = Program('Module', {'body': []})

    # region Statements
    @_("statements")
    def body(self, p):
        self.program.statements['body'] = p.statements

    @_("statement")
    def statements(self, p):
        return [p.statement]
    
    @_("statements statement")
    def statements(self, p):
        p.statements.append(p.statement)
        return p.statements
    
    @_("RETURN expr")
    def statement(self, p):
        return ReturnStatement(p.expr)
    
    @_('FN IDENT LPAREN fn_params RPAREN ARROW IDENT LBRACE statements RBRACE')
    def statement(self, p):
        return FunctionStatement(
            name=p.IDENT0,
            return_type=p.IDENT1,
            body=p.statements,
            params=p.fn_params if p.fn_params else []
        )

    # @_('IF expr LBRACE statements RBRACE')
    # def statement(self, p):
    #     pass
    
    # @_('IF expr LBRACE statements RBRACE ELSE LBRACE statements RBRACE')
    # def statement(self, p):
    #     pass
    
    # @_('WHILE expr LBRACE statements RBRACE')
    # def statement(self, p):
    #     pass
    
    @_('IDENT EQ expr')
    def statement(self, p):
        return AssignStatement(
            name=p.IDENT,
            value=p.expr
        )
    
    @_('IDENT LPAREN params RPAREN')
    def statement(self, p):
        return CallStatement(
            name=p.IDENT,
            params=p.params
        )
    
    @_('fn_params COMMA fn_param')
    def fn_params(self, p):
        p.fn_params.append(p.fn_param)
        return p.fn_params
    
    @_('fn_param')
    def fn_params(self, p):
        return [p.fn_param]
    
    @_('IDENT COLON IDENT')
    def fn_param(self, p):
        return FunctionParam(
            name=p.IDENT0,
            type=p.IDENT1
        )
    
    @_('')
    def fn_param(self, p):
        return
    
    @_('params COMMA param')
    def params(self, p):
        p.params.append(p.param)
        return p.params
    
    @_('param')
    def params(self, p):
        return [p.param]
    
    @_('expr')
    def param(self ,p):
        return p.expr
    
    @_('')
    def param(self, p):
        return
    # endregion

    # region Expressions
    @_('IDENT LPAREN params RPAREN')
    def expr(self, p):
        return CallStatement(
            name=p.IDENT,
            params=p.params
        )

    @_('expr PLUS expr',
       'expr MINUS expr',
       'expr ASTERISK expr',
       'expr SLASH expr',
       'expr MODULUS expr',
       'expr GT expr',
       'expr GTE expr',
       'expr LT expr',
       'expr LTE expr',
       'expr NOTEQ expr',
       'expr EQEQ expr',
       'expr AND expr',
       'expr OR expr')
    def expr(self, p):
        return BinaryExpression(
            left_side=p[0],
            operator=p[1],
            right_side=p[2]
        )
    
    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr
    
    @_('IDENT')
    def expr(self, p):
        return IdentifierLiteral(value=p.IDENT)
    
    @_('INT')
    def expr(self, p):
        return IntegerLiteral(value=int(p.INT))
    
    @_('MINUS INT')
    def expr(self, p):
        return IntegerLiteral(value=int(p.INT) * -1)
    
    @_('FLOAT')
    def expr(self, p):
        return FloatLiteral(value=float(p.FLOAT))
    
    @_('MINUS FLOAT')
    def expr(self, p):
        return FloatLiteral(value=float(p.FLOAT) * -1)
    
    @_('STRING')
    def expr(self,p):
        return StringLiteral(value=p.STRING)
    # endregion
    
