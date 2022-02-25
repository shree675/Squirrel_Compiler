from sly import Parser as SlyParser
from AstNode import Operator, AstNode
from LexicalAnalysis import lexer
import os

TEST_SUITES_DIR = "..\\TestSuites\\" if os.getcwd().endswith(
    "SyntaxAnalysis") else "TestSuites//"

INT = "int"
FLOAT = "float"
STRING = "string"
BOOL = "bool"
CHAR = "char"

print(os.getcwd())

'''
symbol_table : {
    'identifier_name' : {
        'type' : 'int',
        'size' : 4,
        'line_no' : 1,
        'scope' : 'global',
}

{ id -> 1
    
    int age = 0;

    { id -> 2

        int age = 1;

        { id -> 3

        }

        { id -> 4

        int a;

        }
      
    }
}

symbol_table : [
    {
        identifier_name : 'age',
        ....details,
        scope: 1
        parent_scope: 0
    },
    {
        identifier_name : 'age',
        ....details,
        scope: 2
        parent_scope: 1
    }
]


global = {

    variable : {
        "age" :{ info about age}
        "name" : { info about name}
    }

    sub_scopes : {
        "sub_scope_1" : {
            parent_scope : global
            variable : {
                "age" :{ info about age}
                "name" : { info about name}
            }
            sub_scopes : {
            
            }
        }

        "sub_scope_2" : {
            parent_scope : global
            variable : {
                "age" :{ info about age}
                "name" : { info about name}
            }
            sub_scopes : {
            
            }
        }
    }
}

'''


class Parser(SlyParser):

    def __init__(self):
        self.symbol_table = []
        self.id = 2
        self.scope_id_stack = [0, 1]

        self.num_labels = 0
        self.num_temp = 0

    def get_new_label(self):
        self.num_labels += 1
        return "L" + str(self.num_labels - 1)

    def get_new_temp(self):
        self.num_temp += 1
        return "t" + str(self.num_temp - 1)

    start = "program"
    tokens = lexer.Lexer.tokens

    debugfile = 'parser.out'

    precedence = (
        ('left', 'COMMA'),
        ('right', 'ASSIGN'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'RELOP2'),
        ('left', 'RELOP1'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIVIDE', 'MOD'),
        ('right', 'TYPECASTING'),         # fictitious token
        ('right', 'UMINUS', 'NOT'),       # fictitious token
        ('right', 'PAREN')                # fictitious token
    )

    # program -> methods
    @_('methods')
    def program(self, p):
        val = AstNode(Operator.A_ROOT, left=p.methods)
        AstNode.generateCode(val, self.get_new_label, self.get_new_temp)

    # methods -> methods method
    @_('methods method')
    def methods(self, p):
        return AstNode(Operator.A_NODE, left=p.methods, right=p.method)

    @_('method')
    def methods(self, p):
        return AstNode(Operator.A_NODE, left=p.method)

    # method -> DATATYPE FUNCNAME ( params ) { statements }
    @_('DATATYPE FUNCNAME LPAREN params RPAREN LBRACE statements RBRACE')
    def method(self, p):
        return AstNode(Operator.A_FUNC, left=p.params, right=p.statements, next_label=self.get_new_label())

    # params -> DATATYPE VARNAME, params | e
    @_('DATATYPE VARNAME COMMA params')
    def params(self, p):
        return None

    @_('empty')
    def params(self, p):
        return None

    # statements -> statements statement
    @_("statements statement")
    def statements(self, p):
        return AstNode(Operator.A_NODE, left=p.statements, right=p.statement)

    @_('empty')
    def statements(self, p):
        return p.empty

    # statement -> declaration_statement | assignment_statement | io_statement | selection_statement | iteration_statement | jump_statement
    @_('declaration_statement SEMICOL')
    def statement(self, p):
        return p.declaration_statement

    @_('assignment_statement SEMICOL')
    def statement(self, p):
        return p.assignment_statement

    @_('io_statement SEMICOL')
    def statement(self, p):
        return p[0]

    @_('selection_statement')
    def statement(self, p):
        return p.selection_statement

    @_('iteration_statement')
    def statement(self, p):
        return p.iteration_statement

    # interation_statement -> while_statement | for_statement
    @_('while_statement')
    def iteration_statement(self, p):
        return p.while_statement

    @_('for_statement')
    def iteration_statement(self, p):
        return p.for_statement

    # while_statement -> WHILE ( expr ) { statements }
    @_('WHILE LPAREN expr RPAREN LBRACE statements RBRACE')
    def while_statement(self, p):
        return AstNode(Operator.A_WHILE, left=p.expr, right=p.statements)

    '''
                        A_NODE
                    1           A_NODE
                           2          A_NODE
                                  4            3
    '''

    # for_statement -> FOR ( for_init ; expr ; assignment_statement ) { statements }
    @_('FOR LPAREN for_init SEMICOL expr SEMICOL assignment_statement RPAREN LBRACE statements RBRACE')
    def for_statement(self, p):
        node_1 = AstNode(Operator.A_NODE, left=p.statements,
                         right=p.assignment_statement)
        node_2 = AstNode(Operator.A_NODE, left=p.expr, right=node_1)
        node_3 = AstNode(Operator.A_NODE, left=p.for_init, right=node_2)
        return node_3

    # for_init -> declaration_statement | assignment_statement
    @_('declaration_statement')
    def for_init(self, p):
        return p.declaration_statement

    @_('assignment_statement')
    def for_init(self, p):
        return p.assignment_statement

    @_("if_statement")
    def selection_statement(self, p):
        return p.if_statement

    # declaration_statement -> simple_init | array_init
    @_("simple_init")
    def declaration_statement(self, p):
        return p.simple_init

    # simple_init -> DATATYPE VARNAME | DATATYPE VARNAME = expr
    @_("DATATYPE VARNAME")
    def simple_init(self, p):

        repeated_vars = filter(
                        lambda var : var["scope"] == self.scope_id_stack[-1] and var["identifier_name"]== p.VARNAME ,
                        self.symbol_table
        )
        if len(repeated_vars) > 0:
            print("Error: Variable already declared in current scope")
            raise Exception(f"Error : variable \"{p.VARNAME}\" already declared in current scope")

        self.symbol_table.append({
            "identifier_name" : p.VARNAME,
            "type" : p.DATATYPE,
            "scope" : self.scope_id_stack[-1],
            "parent_scope": self.scope_id_stack[-2]
        })

        val = AstNode(Operator.A_DECL, left=p.VARNAME)
        val.code = p.DATATYPE + " " + p.VARNAME + " = "
        if p.DATATYPE == INT:
            val.code += "0"
        elif p.DATATYPE == FLOAT:
            val.code += "0.0"
        elif p.DATATYPE == STRING:
            val.code += "\"\""
        elif p.DATATYPE == BOOL:
            val.code += "false"
        elif p.DATATYPE == CHAR:
            val.code += "'0'"
        return val

    @_("DATATYPE VARNAME ASSIGN expr")
    def simple_init(self, p):
        pass

    # if_statement -> IF ( expr ) { statements }
    @_("IF LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close ")
    def if_statement(self, p):
        return AstNode(Operator.A_IF, left=p.expr, right=p.statements)

    # if_statement -> IF ( expr ) { statements } else { statements }
    @_("IF LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close ELSE LBRACE scope_open statements RBRACE scope_close")
    def if_statement(self, p):
        return AstNode(Operator.A_IFELSE, left=p.expr, mid=p.statements0, right=p.statements1)

    # if_statement -> IF ( expr ) { statements} elif
    @_('IF LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close elif_statement')
    def if_statement(self, p):
        return AstNode(Operator.A_IFELSE, left=p.expr, mid=p.statements, right=p.elif_statement)

    # elif -> ELIF ( expr ) { statements } elif | ELIF ( expr ) { statements } | ELIF ( expr ) { statements } ELSE { statements }
    @_("ELIF LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close elif_statement")
    def elif_statement(self, p):
        return AstNode(Operator.A_ELIFMULTIPLE, left=p.expr, mid=p.statements, right=p.elif_statement)

    @_("ELIF LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close")
    def elif_statement(self, p):
        return AstNode(Operator.A_ELIFSINGLE, left=p.expr, right=p.statements)

    @_("ELIF LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close ELSE LBRACE scope_open statements RBRACE scope_close")
    def elif_statement(self, p):
        return AstNode(Operator.A_IFELIFELSE, left=p.expr, mid=p.statements0, right=p.statements1)
    
# ------------------- SCOPING RULES -------------------------
    @_("")
    def scope_open(self, p):
        self.scope_id_stack.append(self.id)
        self.id += 1
    
    @_("")
    def scope_close(self, p):
        self.scope_id_stack.pop()

# ----------------------------------------------------------

    # io_statement -> input_statement | output_statement
    @_('input_statement')
    def io_statement(self, p):
        return p[0]

    @_('output_statement')
    def io_statement(self, p):
        return p[0]

    # input_statement -> INPUT ( left_value )
    @_('INPUT LPAREN left_value RPAREN')
    def input_statement(self, p):
        return str(p[0]+p[1]+p[2]+p[3])

    # output_statement -> OUTPUT ( left_value )  | OUTPUT ( constant )
    @_('OUTPUT LPAREN left_value RPAREN')
    def output_statement(self, p):
        return str(p[0]+p[1]+p[2]+p[3])

    @_('OUTPUT LPAREN constant RPAREN')
    def output_statement(self, p):
        return str(p[0]+p[1]+p[2]+p[3])

    # jump_statement -> BREAK | return_statement
    @_('BREAK')
    def jump_statement(self, p):
        return p.BREAK

    @_('return_statement')
    def jump_statement(self, p):
        return p.return_statement

    # return_statement -> RETURN expr | RETURN
    @_('RETURN expr')
    def return_statement(self, p):
        return str('return ' + p.expr)

    @_('RETURN')
    def return_statement(self, p):
        return str('return')

    @_('expr PLUS expr')
    def expr(self, p):
        '''
            expr0.code
            expr1.code
            t = expr0.addr + expr1.addr
        '''
        return AstNode(Operator.A_PLUS, left=p.expr0, right=p.expr1)

    @_('expr MINUS expr')
    def expr(self, p):
        return AstNode(Operator.A_MINUS, left=p.expr0, right=p.expr1)

    @_('expr MULT expr')
    def expr(self, p):
        return AstNode(Operator.A_MULTIPLY, left=p.expr0, right=p.expr1)

    @_('expr DIVIDE expr')
    def expr(self, p):
        return AstNode(Operator.A_DIVIDE, left=p.expr0, right=p.expr1)

    @_('expr MOD expr')
    def expr(self, p):
        return AstNode(Operator.A_MODULO, left=p.expr0, right=p.expr1)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return AstNode(Operator.A_NEGATE, left=p.expr)

    @_('LPAREN expr RPAREN %prec PAREN')
    def expr(self, p):
        return p.expr

    @_('expr RELOP1 expr')
    def expr(self, p):
        return AstNode(Operator.A_RELOP1, left=p.expr0, right=p.expr1, value=p.RELOP1)

    @_('expr RELOP2 expr')
    def expr(self, p):
        return AstNode(Operator.A_RELOP2, left=p.expr0, right=p.expr1, value=p.RELOP2)

    @_('expr AND expr')
    def expr(self, p):
        return AstNode(Operator.A_AND, left=p.expr0, right=p.expr1)

    @_('expr OR expr')
    def expr(self, p):
        return AstNode(Operator.A_OR, left=p.expr0, right=p.expr1)

    @_('NOT expr')
    def expr(self, p):
        return AstNode(Operator.A_NOT, left=p.expr)

    @_('VARNAME')
    def expr(self, p):
        return AstNode(Operator.A_VARIABLE, value=p.VARNAME)

    # expr -> constant
    @_('constant')
    def expr(self, p):
        return AstNode(Operator.A_BOOLCONST, value=p.constant)

    # expr -> (DATATYPE) expr
    @_('LPAREN DATATYPE RPAREN expr %prec TYPECASTING')
    def expr(self, p):
        return str('('+p[0]+p[1]+p[2]+p[3]+')')

    # arr_variable -> VARNAME [INTVAL] | VARNAME [INTVAL][INTVAL] | VARNAME [VARNAME] | VARNAME [VARNAME][VARNAME] | VARNAME [INTVAL][VARNAME] | VARNAME [VARNAME][INTVAL]
    @_('VARNAME LSQB INTVAL RSQB')
    def array_variable(self, p):
        '''return {
            "code"
            "addr"
            "rows"
            "columns"
        }'''
        return str('('+p[0]+'['+p[2]+']'+')')

    @_('VARNAME LSQB INTVAL RSQB LSQB INTVAL RSQB')
    def array_variable(self, p):
        return str('('+p[0]+'['+p[2]+']['+p[5]+']'+')')

    @_('VARNAME LSQB VARNAME RSQB')
    def array_variable(self, p):
        return str('('+p[0]+'['+p[2]+']'+')')

    @_('VARNAME LSQB VARNAME RSQB LSQB INTVAL RSQB')
    def array_variable(self, p):
        return str('('+p[0]+'['+p[2]+']['+p[5]+']'+')')

    @_('VARNAME LSQB INTVAL RSQB LSQB VARNAME RSQB')
    def array_variable(self, p):
        return str('('+p[0]+'['+p[2]+']['+p[5]+']'+')')

    @_('VARNAME LSQB VARNAME RSQB LSQB VARNAME RSQB')
    def array_variable(self, p):
        return str('('+p[0]+'['+p[2]+']['+p[5]+']'+')')

    # assignment_statement -> left_value = expr
    @_('left_value ASSIGN expr')
    def assignment_statement(self, p):
        # TODO: update this
        try:
            return AstNode(Operator.A_ASSIGN_STMT, left=p.left_value[1], right=p.expr)
        except:
            return AstNode(Operator.A_ASSIGN_STMT, left=p.left_value, right=p.expr)

    # left_value -> VARNAME | array_variable
    @_('VARNAME')
    def left_value(self, p):
        return ["varname", str(p[0])]

    @_('array_variable')
    def left_value(self, p):
        return str(p[0])

    # constant -> INTVAL | FLOATVAL | CHARVAL | STRINGVAL | BOOLVAL
    @_('INTVAL')
    def constant(self, p):
        return str(p[0])

    @_('FLOATVAL')
    def constant(self, p):
        return str(p[0])

    @_('CHARVAL')
    def constant(self, p):
        return str(p[0])

    @_('STRINGVAL')
    def constant(self, p):
        return str(p[0])

    @_('BOOLVAL')
    def constant(self, p):
        return p.BOOLVAL

    # expr -> function_call
    @_('function_call')
    def expr(self, p):
        return str(p.function_call)

    # function_call -> VARNAME ( argument_list )
    @_('VARNAME LPAREN argument_list RPAREN')
    def function_call(self, p):
        return str(p[0]+p[1]+p[2]+p[3])

    # argument_list -> argument, argument_list
    @_('argument COMMA argument_list')
    def argument_list(self, p):
        return str(p[0]+p[1]+p[2])

    # argument_list -> argument
    @_('argument')
    def argument_list(self, p):
        return str(p.argument)

    # argument -> VARNAME | constant | array_variable
    @_('VARNAME',
        'constant',
        'array_variable')
    def argument(self, p):
        return str(p[0])

    @_('')
    def empty(self, p):
        val = AstNode()
        val.code = ""
        return val

    # def error(self, p):
        # if p:
        #print("Syntax error at line", p.lineno, "| TOKEN:", p.value)
        #
        # else:
        #print("Syntax error at EOF")
        #raise Exception('Syntax error')


if __name__ == '__main__':

    lex = lexer.Lexer()
    parser = Parser()

    with open(TEST_SUITES_DIR + "TACtest2.sq", 'r') as f:
        text = f.read()

    parser.parse(lex.tokenize(text))
