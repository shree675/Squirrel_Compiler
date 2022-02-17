from sly import Parser as SlyParser
import sys
import os
sys.path.append(os.path.abspath('../LexicalAnalysis'))
import lexer

'''
symbol_table : {
    'identifier_name' : {
        'type' : 'int',
        'size' : 4,
        'line_no' : 1,
        'scope' : 'global',
    }
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
        self.t = 0
    
    debugfile = 'parser.out'
    tokens = lexer.Lexer.tokens

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


    
    # statements -> statement; statements | e 
    @_("statement statements")
    def statements(self, p):
        return p[0]

    @_("")
    def statements(self, p):
        return None

    # temporary
    # statement -> expr
    #@_('expr')
    #def statement(self, p):
        #return p.expr
    
    # statement -> declaration_statement | assignment_statement | io_statement | selection_statement | iteration_statement | jump_statement
    @_('declaration_statement SEMICOL')
    def statement(self, p):
        return p[0]

    @_('assignment_statement SEMICOL')
    def statement(self, p):
        return p[0]

    @_('io_statement SEMICOL')
    def statement(self, p):
        return p[0]

    @_('if_statement')
    def statement(self, p):
        return p[0]

    # @_('selection_statement')
    # def statement(self, p):
    #     return p.[0]

    # @_('iteration_statement')
    # def statement(self, p):
    #     return p.[0]

    # @_('jump_statement')
    # def statement(self, p):
    #     return p.[0]

    # declaration_statement -> simple_init | array_init
    @_("simple_init")
    def declaration_statement(self, p):
        return 0

    # simple_init -> DATATYPE VARNAME | DATATYPE VARNAME = expr
    @_("DATATYPE VARNAME")
    def simple_init(self, p):
        cur_scope_vars = filter(lambda e : e["scope"] == self.scope_id_stack[-1] ,self.symbol_table)
        for var in cur_scope_vars:
            if var["identifier_name"] == p[1]:
                print("Error: Variable already declared in current scope")
                raise Exception(f"Error : variable \"{p[1]}\" already declared in current scope")

        self.symbol_table.append({
            "identifier_name" : p[1],
            "type" : p[0],
            "scope" : self.scope_id_stack[-1],
            "parent_scope": self.scope_id_stack[-2]
        })


    # if_statement -> IF ( expr ) { statements if_close }
    @_("IF LPAREN expr RPAREN LBRACE if_open statements if_close RBRACE")
    def if_statement(self, p):
        return p[0]

    @_("")
    def if_open(self, p):
        self.scope_id_stack.append(self.id)
        self.id += 1

    @_("")
    def if_close(self, p):
        self.scope_id_stack.pop()
        

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
        addr = 't'+str(self.t)
        self.t += 1

        return {
            "addr" : addr,
            "code" : p.expr0["code"] + p.expr1["code"] + f"{addr} = {p.expr0['addr']} + {p.expr1['addr']}" + "\n"
        }

    @_('expr MINUS expr')
    def expr(self, p):

        addr = 't'+str(self.t)
        self.t += 1

        return {
            "addr" : addr,
            "code" : p.expr0["code"] + p.expr1["code"] + f"{addr} = {p.expr0['addr']} - {p.expr1['addr']}" + "\n"
        }

        return str('('+p.expr0+'-'+p.expr1+')')

    @_('expr MULT expr')
    def expr(self, p):

        addr = 't'+str(self.t)
        self.t += 1

        return {
            "addr" : addr,
            "code" : p.expr0["code"] + p.expr1["code"] + f"{addr} = {p.expr0['addr']} * {p.expr1['addr']}" + "\n"
        }

    @_('expr DIVIDE expr')
    def expr(self, p):

        addr = 't'+str(self.t)
        self.t += 1

        return {
            "addr" : addr,
            "code" : p.expr0["code"] + p.expr1["code"] + f"{addr} = {p.expr0['addr']} / {p.expr1['addr']}" + "\n"
        }

    @_('expr MOD expr')
    def expr(self, p):

        addr = 't'+str(self.t)
        self.t += 1

        return {
            "addr" : addr,
            "code" : p.expr0["code"] + p.expr1["code"] + f"{addr} = {p.expr0['addr']} % {p.expr1['addr']}" + "\n"
        }


    @_('MINUS expr %prec UMINUS')
    def expr(self, p):

        addr = 't'+str(self.t)
        self.t += 1

        return {
            "addr" : addr,
            "code": p.expr["code"] + f"{addr} = -{p.expr['addr']}" + "\n"
        }

    @_('LPAREN expr RPAREN %prec PAREN')
    def expr(self, p):
        return p.expr
    
 
    
    @_('expr RELOP1 expr')
    def expr(self, p):
        return str('('+p.expr0+p[1]+p.expr1+')')

    @_('expr RELOP2 expr')
    def expr(self, p):
        return str('('+p.expr0+p[1]+p.expr1+')')


    @_('expr AND expr')
    def expr(self, p):
        return str('('+p.expr0+p[1]+p.expr1+')')

    @_('expr OR expr')
    def expr(self, p):
        return str('('+p.expr0+p[1]+p.expr1+')')

    @_('NOT expr %prec NOT')
    def expr(self, p):
        return str('(!'+p.expr+')')

    @_('VARNAME')
    def expr(self, p):
        return {
            "addr" : str(p[0]),
            "code" : ""
        }

    # expr -> constant
    @_('constant')
    def expr(self, p):
        return {
            "addr" : str(p[0]),
            "code" : ""
        }

    # expr -> (DATATYPE) expr
    @_('LPAREN DATATYPE RPAREN expr %prec TYPECASTING')
    def expr(self, p):
        return str('('+p[0]+p[1]+p[2]+p[3]+')')

# -----------------------------------------------------------------------------------------

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
        return p.expr["code"] + str(p.left_value + '=' + p.expr["addr"]) + "\n"

    # left_value -> VARNAME | array_variable
    @_('VARNAME')
    def left_value(self, p):
        return str(p[0])

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
        return str(p[0]) 

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

    def error(self, p):
        if p:
            print("Syntax error at line", p.lineno, "| TOKEN:", p.value)
            self.errok()
        else:
            print("Syntax error at EOF")
        raise Exception('Syntax error')


if __name__ == '__main__':


    lex = lexer.Lexer()
    parser = Parser()


    while True:
        # try:
            # text = input('calc > ')
            file = open("../TestSuites/TACtest.sq", 'r')
            text = file.read()
            result = parser.parse(lex.tokenize(text))
            print(result)
            # print(parser.symbol_table)
            break
        # except:
            # print('Error')
            # break
