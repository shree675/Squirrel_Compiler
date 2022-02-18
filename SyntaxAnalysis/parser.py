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
        self.temp = -1
        self.label = -1
        self.next_label_stack = []
        self.cond_label_stack = []

    
    def gen_temp(self):
        self.temp += 1
        return "t"+str(self.temp)

    def gen_label(self):
        self.label += 1
        return "L"+str(self.label)
        

    
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
        print("statements")
        return {
            "code" : p.statement["code"] + p.statements["code"],
        }

    @_("")
    def statements(self, p):
        return {
            "code" : "",
        }

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
        return {
            "code" : p.assignment_statement["code"]
        }

    @_('io_statement SEMICOL')
    def statement(self, p):
        return p[0]


    @_('start_selection selection_statement')
    def statement(self, p):
        self.next_label_stack.pop()
        print("statement")
        return {
            "code" : p.selection_statement["code"] + p.selection_statement["next"] + "\n",
        }
    
    @_("")
    def start_selection(self, p):
        self.next_label_stack.append(self.gen_label())
    
    @_("if_statement")
    def selection_statement(self, p):
        print("selection_statement")
        return {
            "code" : p.if_statement["code"],
            "next" : self.next_label_stack[-1],
        }

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

    # @_("IF LPAREN if_paren_open_and expr AND expr RPAREN LBRACE if_open statements if_close RBRACE")
    # def if_statement(self, p):
        # return {
            # # "code" : p.expr["code"] + p.statements["code"],
            # "code" : ""
        # }

    # @_("IF LPAREN if_paren_open_or expr OR expr RPAREN LBRACE if_open statements if_close RBRACE")
    # def if_statement(self, p):
        # return {
            # # "code" : p.expr["code"] + p.statements["code"],
            # "code" : ""
        # }
    
    # @_("")
    # def if_paren_open_and(self, p):
        # self.cond_label_stack.append({"true" : self.gen_label(), "false" : self.next_label_stack[-1]})
        # print("b1_open")
        # self.cond_label_stack.append({"true" : self.gen_label(), "false" : self.cond_label_stack[-1]["false"]})
        # return {
            # "true" : self.cond_label_stack[-1]["true"],
            # "false" : self.cond_label_stack[-1]["false"]
        # }

    # @_("")
    # def if_paren_open_or(self, p):
        # self.cond_label_stack.append({"true" : self.gen_label(), "false" : self.next_label_stack[-1]})


    # if_statement -> IF ( expr ) { statements if_close }
    @_("IF if_paren_open LPAREN expr RPAREN LBRACE if_open statements if_close RBRACE")
    def if_statement(self, p):
        print("if_statement")
        return {
            "code" : p.expr["code"] + self.cond_label_stack[-1]["true"] + "\n" + p.statements["code"],
            # "code" : ""
        }
    
    @_("bool_expr PLUS expr")
    def bool_expr(self, p):

        addr = self.gen_temp()

        return {
            "addr" : addr,
            "code" : p.bool_expr["code"] + p.expr["code"] + f"{addr} = {p.bool_expr['addr']} + {p.expr['addr']}" + "\n"
        }
    
    @_("constant")
    def bool_expr(self, p):
        return p.constant

    @_("")
    def if_open(self, p):
        self.scope_id_stack.append(self.id)
        self.id += 1

    @_("")
    def if_close(self, p):
        self.scope_id_stack.pop()
        self.cond_label_stack.pop()
    
    @_("")
    def if_paren_open(self, p):
        self.cond_label_stack.append({"true" : self.gen_label(), "false" : self.next_label_stack[-1]})

        # print("b1_open")
        # self.cond_label_stack.append({"true" : self.gen_label(), "false" : self.cond_label_stack[-1]["false"]})
        # return {
            # "true" : self.cond_label_stack[-1]["true"],
            # "false" : self.cond_label_stack[-1]["false"]
        # }
        

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
        addr = self.gen_temp()

        return {
            "addr" : addr,
            "code" : p.expr0["code"] + p.expr1["code"] + f"{addr} = {p.expr0['addr']} + {p.expr1['addr']}" + "\n"
        }

    @_('expr MINUS expr')
    def expr(self, p):

        addr = self.gen_temp()

        return {
            "addr" : addr,
            "code" : p.expr0["code"] + p.expr1["code"] + f"{addr} = {p.expr0['addr']} - {p.expr1['addr']}" + "\n"
        }


    @_('expr MULT expr')
    def expr(self, p):

        addr = self.gen_temp()

        return {
            "addr" : addr,
            "code" : p.expr0["code"] + p.expr1["code"] + f"{addr} = {p.expr0['addr']} * {p.expr1['addr']}" + "\n"
        }

    @_('expr DIVIDE expr')
    def expr(self, p):

        addr = self.gen_temp()

        return {
            "addr" : addr,
            "code" : p.expr0["code"] + p.expr1["code"] + f"{addr} = {p.expr0['addr']} / {p.expr1['addr']}" + "\n"
        }

    @_('expr MOD expr')
    def expr(self, p):

        addr = self.gen_temp()

        return {
            "addr" : addr,
            "code" : p.expr0["code"] + p.expr1["code"] + f"{addr} = {p.expr0['addr']} % {p.expr1['addr']}" + "\n"
        }


    @_('MINUS expr %prec UMINUS')
    def expr(self, p):

        addr = self.gen_temp()
        
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

  

    @_('b1_open expr b2_open AND expr')
    def expr(self, p):
        print("b1_open expr b2_open OR expr")
        return {
            "code" : p.expr0["code"] + p.b1_open["true"] + "\n" + p.expr1["code"]
            # "code" : p.expr1["code"]
        } 
    
    @_("COMMA")
    def b1_open(self, p):
        print("b1_open")
        self.cond_label_stack.append({"true" : self.gen_label(), "false" : self.cond_label_stack[-1]["false"]})
        return {
            "true" : self.cond_label_stack[-1]["true"],
            "false" : self.cond_label_stack[-1]["false"]
        }

    @_('')
    def b2_open(self, p):
        print("b2_open")
        self.cond_label_stack.pop()
        self.cond_label_stack.append({"true" : self.cond_label_stack[-1]["true"], "false" : self.cond_label_stack[-1]["false"]})

    # @_('expr OR expr')
    # def expr(self, p):
        # print('expr OR expr')
        # return str('('+p.expr0+p[1]+p.expr1+')')

    @_('NOT expr %prec NOT')
    def expr(self, p):
        print('NOT expr %prec NOT')
        return str('(!'+p.expr+')')

    @_('VARNAME')
    def expr(self, p):
        print("varname : " + p.VARNAME)
        return {
            "addr" : p.VARNAME,
            "code" : ""
        }

    # expr -> constant
    @_('constant')
    def expr(self, p):
        print("constant " + p.constant["val"])
        return {
            "addr" : p.constant["val"],
            "code" : p.constant["code"]
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
        return {
            "code" : p.expr["code"] + str(p.left_value + '=' + p.expr["addr"]) + "\n"
        }
        

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
        return {
            "val" : p.BOOLVAL,
            "code" : "goto " + self.cond_label_stack[-1][p.BOOLVAL] + "\n"
        }

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

    #def error(self, p):
        #if p:
            #print("Syntax error at line", p.lineno, "| TOKEN:", p.value)
            #self.errok()
        #else:
            #print("Syntax error at EOF")
        #raise Exception('Syntax error')


if __name__ == '__main__':


    lex = lexer.Lexer()
    parser = Parser()


    while True:
        # try:
            # text = input('calc > ')
            file = open("../TestSuites/TACtest.sq", 'r')
            text = file.read()
            result = parser.parse(lex.tokenize(text))
            print(result["code"])
            # print(parser.symbol_table)
            break
        # except:
            # print('Error')
            # break
