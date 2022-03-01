from sly import Parser as SlyParser
from AstNode import Operator, AstNode
from LexicalAnalysis import lexer
import os

TEST_SUITES_DIR = os.path.join("..", "TestSuites") if os.getcwd().endswith(
    "SyntaxAnalysis") else os.path.join("TestSuites")


class Parser(SlyParser):

    def __init__(self):
        self.symbol_table = []
        self.id = 2  # start from 2, as 1 is reserved for global scope
        self.scope_id_stack = [0, 1]
        self.num_labels = 0
        self.num_temp = 0

    def get_new_label(self):
        """Generates and returns a new label, globally unique"""
        self.num_labels += 1
        return "L" + str(self.num_labels - 1)

    def get_new_temp(self):
        """Generates and returns a new temporary variable, globally unique"""
        self.num_temp += 1
        return "t" + str(self.num_temp - 1)

    # dimension = [2, 3] =>  2 rows, 3 cols
    def push_to_ST(self, data_type, varname, dimension):
        """Pushes a new variable to the symbol table"""
        # check if the variable already exists in the same scope
        repeated_vars = list(filter(
            lambda var: var["scope"] == self.scope_id_stack[-1] and var["identifier_name"] == varname,
            self.symbol_table
        ))
        if len(repeated_vars) > 0:
            print("Error: Variable already declared in current scope")
            raise Exception(
                f"Error : variable \"{varname}\" already declared in current scope")
        # else append the variable to the symbol table
        self.symbol_table.append({
            "identifier_name": varname,
            "type": data_type,
            "dimension": dimension,
            "scope": self.scope_id_stack[-1],
            "parent_scope": self.scope_id_stack[-2]
        })

    """The rest of this file conforms to the specifications of SLY, the parsing library used by this project.
    Each function corresponds to a production rule in the grammar. The rule is mentioned as a comment just above 
    corresponding function. SLY works on SDDs, so the body of the method is executed after the entire production is matched"""

    start = "program"  # start symbol of the grammar
    tokens = lexer.Lexer.tokens
    debugfile = 'parser.out'  # SLY parser writes debug information to this file
    precedence = (
        ('left', 'COMMA'),
        ('right', 'ASSIGN'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'RELOP2'),
        ('left', 'RELOP1'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIVIDE', 'MOD'),
        # fictitious token used to handle special precedence rules
        ('right', 'TYPECASTING'),
        # fictitious token used to handle special precedence rules
        ('right', 'UMINUS', 'NOT'),
        # fictitious token used to handle special precedence rules
        ('right', 'PAREN')
    )

    # program -> methods
    @_('methods')
    def program(self, p):
        """Starting production, top of the parsing tree, calls the recursive generateCode() method"""
        val = AstNode(Operator.A_ROOT, left=p.methods)
        AstNode.generateCode(val, self.get_new_label,
                             self.get_new_temp, self.symbol_table)
        # print(val.code)
        print(self.symbol_table)

    # methods -> methods method
    @_('methods method')
    def methods(self, p):
        return AstNode(Operator.A_NODE, left=p.methods, right=p.method)

    @_('method')
    def methods(self, p):
        return AstNode(Operator.A_NODE, left=p.method)

    # method -> DATATYPE FUNCNAME ( params ) { statements }
    @_('DATATYPE FUNCNAME LPAREN scope_open params RPAREN LBRACE statements RBRACE scope_close')
    def method(self, p):
        return AstNode(Operator.A_FUNC, left=p.params, right=p.statements, next_label=self.get_new_label())

    # params -> DATATYPE VARNAME COMMA params | e
    # params -> params_rec | e
    # params_rec -> DATATYPE VARNAME COMMA params_rec | DATATYPE VARNAME

    @_('params_rec')
    def params(self, p):
        return None

    @_('empty')
    def params(self, p):
        return None

    @_('DATATYPE VARNAME COMMA params_rec')
    def params_rec(self, p):
        self.push_to_ST(p.DATATYPE, p.VARNAME, [])

    @_('DATATYPE VARNAME')
    def params_rec(self, p):
        self.push_to_ST(p.DATATYPE, p.VARNAME, [])

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
        return AstNode(Operator.A_FORPARENT, left=p.for_statement)

    # while_statement -> WHILE ( expr ) { statements }
    @_('WHILE LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close')
    def while_statement(self, p):
        return AstNode(Operator.A_WHILE, left=p.expr, right=p.statements)

    # for_statement -> FOR ( for_init ; expr ; assignment_statement ) { statements }
    @_('FOR LPAREN scope_open for_init SEMICOL expr SEMICOL assignment_statement RPAREN LBRACE statements RBRACE scope_close')
    def for_statement(self, p):
        node_1 = AstNode(Operator.A_FOR, left=p.expr,
                         mid=p.assignment_statement, right=p.statements)
        node_2 = AstNode(Operator.A_NODE, left=p.for_init, right=node_1)
        return node_2

    # for_init -> declaration_statement | assignment_statement
    @_('declaration_statement')
    def for_init(self, p):
        return p.declaration_statement

    @_('assignment_statement')
    def for_init(self, p):
        return p.assignment_statement

    @_("if_statement")
    def selection_statement(self, p):
        return AstNode(Operator.A_IFPARENT, p.if_statement)

    @_('switch_statement')
    def selection_statement(self, p):
        return AstNode(Operator.A_SWITCHPARENT, left=p.switch_statement)

    # TODO : ST for array_init
    # declaration_statement -> simple_init | array_init
    @_("simple_init")
    def declaration_statement(self, p):
        return p.simple_init

    @_("array_init")
    def declaration_statement(self, p):
        return p.array_init

    # simple_init -> DATATYPE VARNAME | DATATYPE VARNAME = expr
    @_("DATATYPE VARNAME")
    def simple_init(self, p):
        self.push_to_ST(p.DATATYPE, p.VARNAME, [])
        return AstNode(Operator.A_DECL, left=[p.DATATYPE, p.VARNAME])

    @_("DATATYPE VARNAME ASSIGN expr")
    def simple_init(self, p):
        self.push_to_ST(p.DATATYPE, p.VARNAME, [])
        return AstNode(Operator.A_DECL, left=[p.DATATYPE, p.VARNAME], right=p.expr)

# ----------------------- ARRAY INIT ---------------------------

    # # array_init -> DATATYPE VARNAME [INTVAL] = { array_list }
    # # if array_list is empty, then the corresponding ASTNode will be None
    # @_("DATATYPE VARNAME LSQB INTVAL RSQB ASSIGN LBRACE array_list RBRACE")
    # def array_init(self, p):
    #     self.push_to_ST(p.DATATYPE, p.VARNAME, [int(p.INTVAL)])
    #     return AstNode(Operator.A_ARR_DECL, left=[p.DATATYPE, p.VARNAME, [int(p.INTVAL)]], right=p.array_list)

    # # array_init -> DATATYPE VARNAME [INTVAL] [INTVAL] = { array_list }
    # @_("DATATYPE VARNAME LSQB INTVAL RSQB LSQB INTVAL RSQB ASSIGN LBRACE array_list RBRACE")
    # def array_init(self, p):
    #     self.push_to_ST(p.DATATYPE, p.VARNAME, [int(p[3]), int(p[6])])
    #     return AstNode(Operator.A_ARR_DECL, left=[p.DATATYPE, p.VARNAME, [int(p[3]), int(p[6])]], right=p.array_list)

    # # array_init -> DATATYPE VARNAME [] [INTVAL] = { array_list }
    # @_("DATATYPE VARNAME LSQB RSQB LSQB INTVAL RSQB ASSIGN LBRACE array_list RBRACE")
    # def array_init(self, p):
    #     self.push_to_ST(p.DATATYPE, p.VARNAME, [-1, int(p[5])])
    #     return AstNode(Operator.A_ARR_DECL, left=[p.DATATYPE, p.VARNAME, [-1, int(p[5])], self.scope_id_stack[-1]], right=p.array_list)

    # array_init -> DATATYPE VARNAME array_rec [INTVAL] = { array_list }
    @_("DATATYPE VARNAME array_rec ASSIGN LBRACE array_list RBRACE")
    def array_init(self, p):
        self.push_to_ST(p.DATATYPE, p.VARNAME, p.array_rec.value)
        return AstNode(Operator.A_ARR_DECL, left=p.array_rec, right=p.array_list, data_type=p.DATATYPE, value=p.VARNAME)

    # array_rec -> array_rec [INTVAL] | e
    @_("array_rec LSQB INTVAL RSQB")
    def array_rec(self, p):
        return AstNode(Operator.A_ARRAY_REC, left=p.array_rec, value=[*p.array_rec.value, int(p.INTVAL)])

    @_("LSQB INTVAL RSQB")
    def array_rec(self, p):
        return AstNode(Operator.A_ARRAY_REC, value=[int(p.INTVAL)])

# ------------------- ARRAY LIST ---------------------------------------

    # array_list = constant, array_list | constant

    @_("array_list_rec")
    def array_list(self, p):
        return p.array_list_rec

    @_("empty")
    def array_list(self, p):
        return None

    @_("constant")
    def array_list_rec(self, p):
        return AstNode(Operator.A_ARR_LITERAL, left=p.constant)

    @_("constant COMMA array_list_rec")
    def array_list_rec(self, p):
        return AstNode(Operator.A_ARR_LITERAL, left=p.constant, right=p.array_list_rec)

# ---------------------------------------------------------------------------

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

    # switch_statement -> SWITCH ( left_value ) { case_statements }
    @_('SWITCH LPAREN left_value RPAREN LBRACE scope_open case_statements RBRACE scope_close')
    def switch_statement(self, p):
        # TODO: update this
        try:
            return AstNode(Operator.A_SWITCH, left=p.left_value[1], right=p.case_statements)
        except:
            return AstNode(Operator.A_SWITCH, left=p.left_value, right=p.case_statements)

    # case_statements -> case_statement case_statements | case_statement | default_statement
    @_('case_statement case_statements')
    def case_statements(self, p):
        return AstNode(Operator.A_CASEMULTIPLE, left=p.case_statement, right=p.case_statements)

    @_('case_statement')
    def case_statements(self, p):
        return p.case_statement

    @_('default_statement')
    def case_statements(self, p):
        return p.default_statement

    # case_statement -> CASE ( constant ) COLON statements
    @_('CASE LPAREN constant RPAREN COLON scope_open statements scope_close')
    def case_statement(self, p):
        return AstNode(Operator.A_CASESINGLE, left=p.constant, right=p.statements)

    # default_statement -> DEFAULT COLON statements
    @_('DEFAULT COLON scope_open statements scope_close')
    def default_statement(self, p):
        return AstNode(Operator.A_DEFAULT, left=p.statements)

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
        return AstNode(p.constant[0], value=p.constant[1])

    # expr -> (DATATYPE) expr
    @_('LPAREN DATATYPE RPAREN expr %prec TYPECASTING')
    def expr(self, p):
        return str('('+p[0]+p[1]+p[2]+p[3]+')')

    # array_variable -> VARNAME array_variable_rec
    @_('VARNAME array_variable_rec')
    def array_variable(self, p):
        return AstNode(Operator.A_ARRAY_VARIABLE, left=p.array_variable_rec, value=p.VARNAME)

    # array_variable_rec -> array_variable_rec [expr] | [expr]
    @_('LSQB expr RSQB array_variable_rec')
    def array_variable_rec(self, p):
        return AstNode(Operator.A_ARRAY_VARIABLE_REC, left=p.array_variable_rec, right=p.expr)

    @_('empty')
    def array_variable_rec(self, p):
        # return AstNode(Operator.A_ARRAY_VARIABLE_REC, left=p.expr)
        pass

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

    # array_variable -> VARNAME [expr] | VARNAME [expr][expr]
    @_('VARNAME LSQB expr RSQB')
    def array_variable(self, p):
        return AstNode(Operator.A_ARR_SINGLE, left=p.VARNAME, right=p.expr)

    # constant -> INTVAL | FLOATVAL | CHARVAL | STRINGVAL | BOOLVAL
    @_('INTVAL')
    def constant(self, p):
        # return AstNode(Operator.A_INTCONST, value=p.INTVAL)
        return [Operator.A_INTCONST, p.INTVAL]

    @_('FLOATVAL')
    def constant(self, p):
        return [Operator.A_FLOATCONST, p.FLOATVAL]

    @_('CHARVAL')
    def constant(self, p):
        return [Operator.A_CHARCONST, p.CHARVAL]

    @_('STRINGVAL')
    def constant(self, p):
        return [Operator.A_STRINGCONST, p.STRINGVAL]

    @_('BOOLVAL')
    def constant(self, p):
        return [Operator.A_BOOLCONST, p.BOOLVAL]

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

    with open(os.path.join(TEST_SUITES_DIR, "ArrayInittest.sq"), 'r') as f:
        text = f.read()

    parser.parse(lex.tokenize(text))
