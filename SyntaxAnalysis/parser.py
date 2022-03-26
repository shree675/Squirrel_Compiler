import warnings
from sly import Parser as SlyParser
from AstNode.AstNode import Operator, AstNode
from SemanticAnalysis import TypeChecker
from LexicalAnalysis import lexer
import os
import re
import logging as logger
logger.exception = logger.error
warnings.filterwarnings("ignore")

TEST_SUITES_DIR = os.path.join("..", "TestSuites") if os.getcwd().endswith(
    "SyntaxAnalysis") else os.path.join("TestSuites")


class Parser(SlyParser):

    def __init__(self):
        self.symbol_table = []
        self.id = 2  # start from 2, as 1 is reserved for global scope
        self.scope_id_stack = [0, 1]
        self.num_labels = 0
        self.num_temp = 0
        self.num_ftemp = 0
        self.type_checker = TypeChecker.TypeChecker(self.symbol_table)
        self.function_symbol_table = []

        '''
            function_symbol_table = [
               {
                   "return_type" : "int",
                   "name" : "start",
                   "parameters_types" : ["int", "float", "char"]

               } 
            ]
        '''

    @staticmethod
    def error(message="Syntax Error"):
        """Function to raise custom errors for the parser, suppressing the stack trace, takes the error message as parameter"""
        try:
            raise Exception(message)   # raise exception with message
        except Exception as ex:
            logger.exception(ex)
            quit()

    def get_new_label(self):
        """Generates and returns a new label, globally unique"""
        self.num_labels += 1
        return "L" + str(self.num_labels - 1)

    def get_new_temp(self, data_type):
        """Generates and returns a new temporary variable, globally unique"""
        if data_type == "float":
            self.num_ftemp += 1
            return "tf" + str(self.num_ftemp - 1)
        else:
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
            Parser.error(
                f"Error : variable \"{varname}\" already declared in current scope")
        # else append the variable to the symbol table
        self.symbol_table.append({
            "identifier_name": varname,
            "type": data_type,
            "dimension": dimension,
            "scope": self.scope_id_stack[-1],
            # "parent_scope": self.scope_id_stack[-2]
        })

    def push_to_FST(self, return_type,  function_name, parameters_types):
        repeated = list(filter(lambda e: e["function_name"] == function_name and
                               e["parameters_types"] == parameters_types,
                               self.function_symbol_table))

        if len(repeated) > 0:
            Parser.error(
                f"The function {function_name}({','.join(parameters_types)}) is already defined.\n")

        self.function_symbol_table.append({
            "return_type": return_type,
            "function_name": function_name,
            "parameters_types": parameters_types
        })

        return

    # this method should be used in parser.py ONLY
    def get_data_type(self, varname):

        i = -1
        current_scope = self.scope_id_stack[i]

        res = []
        while current_scope >= 1 and len(res) == 0:

            res = list(filter(
                lambda item: item["scope"] == current_scope and item["identifier_name"] == varname,
                self.symbol_table
            ))

            i -= 1
            current_scope = self.scope_id_stack[i]

        if(len(res) == 1):
            # print(res[0]["type"])
            return res[0]["type"]
        else:
            Parser.error(
                f"Error : variable \"{varname}\" not declared in the scope")

    def check_function_signature(self, function_name, args_types):

        matched = list(filter(lambda e: e["function_name"] == "@"+function_name and
                              e["parameters_types"] == args_types,
                              self.function_symbol_table))

        if len(matched) == 0:
            Parser.error(f"Semantic error : function call {function_name}({','.join(args_types)})"
                         + " doesn't match any of the defined function signatures.\n")

    def check_if_variable(self, varname):
        i = -1
        current_scope = self.scope_id_stack[i]

        res = []
        while current_scope >= 1 and len(res) == 0:

            res = list(filter(
                lambda item: item["scope"] == current_scope and item["identifier_name"] == varname,
                self.symbol_table
            ))

            i -= 1
            current_scope = self.scope_id_stack[i]

        num_dimensions = len(res[0]["dimension"])
        if num_dimensions != 0:
            Parser.error(
                f"Semantic Error: \"{varname}\" is an array variable.")

    def print_tree(self, root):

        #print('\n--- Tree -------------------------------')

        q = [root]
        curl = 1
        nextl = 0

        while len(q) > 0:
            s = q.pop(0)
            curl -= 1

            if isinstance(s, AstNode) and s.operator:
                print(s.operator.value, end=' ')
            if isinstance(s, list):
                print(s, end=' ')
            if s == None:
                print('None', end=' ')

            if isinstance(s, AstNode) and s.left:
                q.append(s.left)
                nextl = + 1
            if isinstance(s, AstNode) and s.mid:
                q.append(s.mid)
                nextl = + 1
            if isinstance(s, AstNode) and s.right:
                q.append(s.right)
                nextl = + 1

            if curl == 0:
                curl = nextl
                nextl = 0
                # print()

        print('\n--- End Tree -------------------------------\n')

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

    # @_('simple_init program')
    # def program(self, p):
    #     pass

    # program -> methods
    @_('methods')
    def program(self, p):
        """Starting production, top of the parsing tree, calls the recursive generateCode() method"""
        root = AstNode(Operator.A_ROOT, left=p.methods)
        root.output_file = self.output_file
        p.methods.parent = root
        # self.print_tree(root)

        # AstNode.generateCode(root, self.get_new_label,
        # self.get_new_temp, self.symbol_table)

        code = AstNode.generateCode(root, self)
        output_path = self.output_file if os.getcwd().endswith(
            "Squirrel_Compiler") else "../" + self.output_file

        with open(output_path, "w") as f:
            # format code
            output = re.sub(r"\n{3,}", "\n\n", code, flags=re.DOTALL)
            # print(output)
            f.write(output)
        #print(*self.symbol_table, sep="\n")
        #print(*self.function_symbol_table, sep="\n")

    # methods -> methods method
    @_('methods method')
    def methods(self, p):
        head = AstNode(Operator.A_NODE, left=p.methods, right=p.method)
        p.methods.parent = head
        p.method.parent = head
        return head

    @_('method')
    def methods(self, p):
        head = AstNode(Operator.A_NODE, left=p.method)
        p.method.parent = head
        return head

    # method -> DATATYPE FUNCNAME ( params ) { statements }
    @_('function_signature LBRACE statements RBRACE scope_close')
    def method(self, p):
        head = p.function_signature
        head.right = p.statements
        p.statements.parent = head
        return p.function_signature

    @_('DATATYPE FUNCNAME LPAREN scope_open params RPAREN')
    def function_signature(self, p):
        head = AstNode(Operator.A_FUNC, left=p.params,
                       next_label=self.get_new_label(),
                       value={"function_name": p.FUNCNAME[1:], "return_type": p.DATATYPE})

        # no AstNode for params here

        # Push the function to the symbol table
        # p.params is a list of data types of parameters
        self.push_to_FST(p.DATATYPE, p.FUNCNAME, p.params)
        return head

    # params -> DATATYPE VARNAME COMMA params | e
    # params -> params_rec | e
    # params_rec -> DATATYPE VARNAME COMMA params_rec | DATATYPE VARNAME

    @_('params_rec')
    def params(self, p):
        return p.params_rec

    @_('empty')
    def params(self, p):
        return []

    @_('DATATYPE VARNAME COMMA params_rec')
    def params_rec(self, p):
        self.push_to_ST(p.DATATYPE, p.VARNAME, [])
        return [p.DATATYPE, *p.params_rec]

    @_('DATATYPE VARNAME')
    def params_rec(self, p):
        self.push_to_ST(p.DATATYPE, p.VARNAME, [])
        return [p.DATATYPE]

    # statements -> statements statement
    @_("statements statement")
    def statements(self, p):
        head = AstNode(Operator.A_NODE, left=p.statements, right=p.statement)
        p.statements.parent = head

        # print("parent : " + str(p.statements.parent.operator.value))

        p.statement.parent = head
        return head

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

    @_('jump_statement SEMICOL')
    def statement(self, p):
        return p.jump_statement

    @_('function_call SEMICOL')
    def statement(self, p):
        return p.function_call

    # interation_statement -> while_statement | for_statement
    @_('while_statement')
    def iteration_statement(self, p):
        return p.while_statement

    @_('for_statement')
    def iteration_statement(self, p):
        head = AstNode(Operator.A_FORPARENT, left=p.for_statement)
        p.for_statement.parent = head
        return head

    # while_statement -> WHILE ( expr ) { statements }
    @_('WHILE LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close')
    def while_statement(self, p):
        self.type_checker.check_datatype(
            expr_type=p.expr.data_type, operator=Operator.A_WHILE)
        head = AstNode(Operator.A_WHILE, left=p.expr, right=p.statements)
        p.expr.parent = head
        p.statements.parent = head
        return head

    # for_statement -> FOR ( for_init ; expr ; assignment_statement ) { statements }

    @_('FOR LPAREN scope_open for_init SEMICOL expr SEMICOL assignment_statement RPAREN LBRACE statements RBRACE scope_close')
    def for_statement(self, p):
        node_1 = AstNode(Operator.A_FOR, left=p.expr,
                         mid=p.assignment_statement, right=p.statements)
        p.expr.parent = node_1
        p.assignment_statement.parent = node_1
        p.statements.parent = node_1

        node_2 = AstNode(Operator.A_NODE, left=p.for_init,
                         right=node_1)
        node_1.parent = node_2
        p.for_init.parent = node_2
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
        head = AstNode(Operator.A_IFPARENT, p.if_statement)
        p.if_statement.parent = head
        return head

    @_('switch_statement')
    def selection_statement(self, p):
        return AstNode(Operator.A_SWITCHPARENT, left=p.switch_statement)

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
        data_type = self.get_data_type(p.VARNAME)
        node = AstNode(Operator.A_DECL, left=[
                       p.DATATYPE, p.VARNAME], data_type=data_type,)
        node.code = ""
        return node

    @_("DATATYPE VARNAME ASSIGN expr")
    def simple_init(self, p):
        self.push_to_ST(p.DATATYPE, p.VARNAME, [])
        data_type = self.get_data_type(p.VARNAME)
        return AstNode(Operator.A_DECL, left=[p.DATATYPE, p.VARNAME], right=p.expr, data_type=data_type)

# ----------------------- ARRAY INIT ---------------------------------

    # array_init -> DATATYPE VARNAME array_variable = { array_list }
    @_("DATATYPE array_variable ASSIGN LBRACE array_list RBRACE")
    def array_init(self, p):
        if p.DATATYPE == 'string':
            AstNode.raise_error(
                "Semantic Error: String type arrays are not allowed")
        self.push_to_ST(
            p.DATATYPE, p.array_variable.value["varname"], p.array_variable.value["list"])
        return AstNode(Operator.A_ARR_DECL, left=p.array_variable, right=p.array_list, data_type=p.DATATYPE, value=p.array_variable.value["varname"])

    # array_variable -> VARNAME [INTVAL]
    @_("VARNAME LSQB INTVAL RSQB")
    def array_variable(self, p):
        return AstNode(Operator.A_ARRAY_REC, value={"list": [int(p.INTVAL)], "varname": p.VARNAME})

    # array_variable [INTVAL]
    @_("array_variable LSQB INTVAL RSQB")
    def array_variable(self, p):
        return AstNode(Operator.A_ARRAY_REC, left=p.array_variable, value={"list": [*p.array_variable.value["list"], int(p.INTVAL)], "varname": p.array_variable.value["varname"]})

    # array_list -> array_list, constant
    @_("array_list COMMA constant")
    def array_list(self, p):
        return AstNode(Operator.A_ARR_LITERAL, left=p.array_list, right=p.constant)

    @_("array_list COMMA MINUS constant")
    def array_list(self, p):
        if p.constant[0] == Operator.A_STRINGCONST:
            AstNode.raise_error(
                "Semantic Error: String constants are not allowed in arrays")
        if p.constant[0] == Operator.A_CHARCONST or p.constant[0] == Operator.A_BOOLCONST:
            AstNode.raise_error(
                "Semantic Error: MINUS operator is not allowed for boolean values and chars")
        p.constant[1] = "-"+p.constant[1]
        return AstNode(Operator.A_ARR_LITERAL, left=p.array_list, right=p.constant)

    # array_list -> constant
    @_("constant")
    def array_list(self, p):
        #print("The const type", p.constant[0])
        if p.constant[0] == Operator.A_STRINGCONST:
            AstNode.raise_error(
                "Semantic Error: String constants are not allowed in arrays")
        data_type = self.type_checker.return_datatype(operator=p.constant[0])
        return AstNode(Operator.A_ARR_LITERAL, left=p.constant, data_type=data_type)

    @_("MINUS constant")
    def array_list(self, p):
        #print("The const type", p.constant[0])
        # semantic check here to not allow negative strings and chars
        if p.constant[0] == Operator.A_STRINGCONST:
            AstNode.raise_error(
                "Semantic Error: String constants are not allowed in arrays")
        if p.constant[0] == Operator.A_CHARCONST or p.constant[0] == Operator.A_BOOLCONST:
            AstNode.raise_error(
                "Semantic Error: MINUS operator is not allowed for boolean values and chars")
        p.constant[1] = "-"+p.constant[1]
        data_type = self.type_checker.return_datatype(operator=p.constant[0])
        return AstNode(Operator.A_ARR_LITERAL, left=p.constant, data_type=data_type)

    # @_("neg_int_constant")
    # def array_list(self, p):
    #     #print("The const type", p.constant[0])
    #     data_type = self.type_checker.return_datatype(
    #         operator=p.neg_int_constant[0])
    #     return AstNode(Operator.A_ARR_LITERAL, left=p.neg_int_constant, data_type=data_type)

    # @_("neg_float_constant")
    # def array_list(self, p):
    #     #print("The const type", p.constant[0])
    #     data_type = self.type_checker.return_datatype(
    #         operator=p.neg_float_constant[0])
    #     return AstNode(Operator.A_ARR_LITERAL, left=p.neg_float_constant, data_type=data_type)

# ---------------------------------------------------------------------------

    # array_variable -> VARNAME [expr]
    @_("VARNAME LSQB expr RSQB")
    def array_var_use(self, p):
        #print("Array expr type", p.expr.value, p.expr.data_type)

        i = -1
        current_scope = self.scope_id_stack[i]

        res = []
        while current_scope >= 1 and len(res) == 0:

            res = list(filter(
                lambda item: item["scope"] == current_scope and item["identifier_name"] == p.VARNAME,
                self.symbol_table
            ))

            if(len(res) > 0):
                break

            i -= 1
            current_scope = self.scope_id_stack[i]

        self.type_checker.check_datatype(
            expr_type=p.expr.data_type, operator=Operator.A_ARR_EXPR_REC)
        data_type = self.get_data_type(p.VARNAME)
        return AstNode(Operator.A_ARR_EXPR_REC, left=p.expr,
                       value={"varname": p.VARNAME, "val": "",
                              "index": 1, "scope": current_scope},
                       data_type=data_type)

    # array_variable [expr]
    @_("array_var_use LSQB expr RSQB")
    def array_var_use(self, p):
        self.type_checker.check_datatype(
            expr_type=p.expr.data_type, operator=Operator.A_ARR_EXPR_REC)

        return AstNode(
            Operator.A_ARR_EXPR_REC,
            left=p.array_var_use,
            right=p.expr,
            value={
                "varname": p.array_var_use.value["varname"],
                "val": "",
                "index": p.array_var_use.value["index"]+1,
                "scope": p.array_var_use.value["scope"]
            }, data_type=p.array_var_use.data_type)

# ---------------------------------------------------------------------------

    # if_statement -> IF ( expr ) { statements }
    @_("IF LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close ")
    def if_statement(self, p):
        self.type_checker.check_datatype(
            expr_type=p.expr.data_type, operator=Operator.A_IF)
        head = AstNode(Operator.A_IF, left=p.expr, right=p.statements)
        p.expr.parent = head
        p.statements.parent = head
        return head

    # if_statement -> IF ( expr ) { statements } else { statements }
    @_("IF LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close ELSE LBRACE scope_open statements RBRACE scope_close")
    def if_statement(self, p):
        self.type_checker.check_datatype(
            expr_type=p.expr.data_type, operator=Operator.A_IFELSE)
        head = AstNode(Operator.A_IFELSE, left=p.expr,
                       mid=p.statements0, right=p.statements1)
        p.expr.parent = head
        p.statements0.parent = head
        p.statements1.parent = head
        return head

    # if_statement -> IF ( expr ) { statements} elif
    @_('IF LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close elif_statement')
    def if_statement(self, p):
        self.type_checker.check_datatype(
            expr_type=p.expr.data_type, operator=Operator.A_IFELSE)
        head = AstNode(Operator.A_IFELSE, left=p.expr,
                       mid=p.statements, right=p.elif_statement)
        p.expr.parent = head
        p.statements.parent = head
        p.elif_statement.parent = head
        return head

    # elif -> ELIF ( expr ) { statements } elif | ELIF ( expr ) { statements } | ELIF ( expr ) { statements } ELSE { statements }
    @_("ELIF LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close elif_statement")
    def elif_statement(self, p):
        self.type_checker.check_datatype(
            expr_type=p.expr.data_type, operator=Operator.A_ELIFMULTIPLE)
        return AstNode(Operator.A_ELIFMULTIPLE, left=p.expr, mid=p.statements, right=p.elif_statement)

    @_("ELIF LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close")
    def elif_statement(self, p):
        self.type_checker.check_datatype(
            expr_type=p.expr.data_type, operator=Operator.A_ELIFSINGLE)
        return AstNode(Operator.A_ELIFSINGLE, left=p.expr, right=p.statements)

    @_("ELIF LPAREN expr RPAREN LBRACE scope_open statements RBRACE scope_close ELSE LBRACE scope_open statements RBRACE scope_close")
    def elif_statement(self, p):
        self.type_checker.check_datatype(
            expr_type=p.expr.data_type, operator=Operator.A_IFELIFELSE)
        return AstNode(Operator.A_IFELIFELSE, left=p.expr, mid=p.statements0, right=p.statements1)

    # switch_statement -> SWITCH ( left_value ) { case_statements }
    @_('SWITCH LPAREN left_value RPAREN LBRACE scope_open case_statements RBRACE scope_close')
    def switch_statement(self, p):

        if p.left_value.data_type != 'int' and p.left_value.data_type != 'char':
            Parser.error(
                "Switch statement variable must be of type int or char")

        """ try:
            return AstNode(Operator.A_SWITCH, left=p.left_value[1], right=p.case_statements)
        except: """
        head = AstNode(Operator.A_SWITCH, left=p.left_value,
                       right=p.case_statements)
        p.left_value.parent = head
        p.case_statements.parent = head
        return head

    # case_statements -> case_statement case_statements | case_statement | default_statement
    @_('case_statement case_statements')
    def case_statements(self, p):
        head = AstNode(Operator.A_CASEMULTIPLE,
                       left=p.case_statement, right=p.case_statements)
        p.case_statement.parent = head
        p.case_statements.parent = head
        return head

    @_('case_statement')
    def case_statements(self, p):
        return p.case_statement

    @_('default_statement')
    def case_statements(self, p):
        return p.default_statement

    # case_statement -> CASE ( constant ) COLON statements
    @_('CASE LPAREN constant RPAREN COLON scope_open statements scope_close')
    def case_statement(self, p):
        #print("P constant", p.constant[0])
        if p.constant[0] != Operator.A_INTCONST and p.constant[0] != Operator.A_CHARCONST:
            Parser.error("Case statement variable must be of type int or char")
        head = AstNode(Operator.A_CASESINGLE,
                       left=p.constant, right=p.statements)
        p.statements.parent = head
        return head

    @_('CASE LPAREN MINUS constant RPAREN COLON scope_open statements scope_close')
    def case_statement(self, p):
        #print("P constant", p.constant[0])
        # semantic check here to not allow negative strings and chars
        if p.constant[0] != Operator.A_INTCONST and p.constant[0] != Operator.A_CHARCONST:
            Parser.error("Case statement variable must be of type int or char")
        if p.constant[0] == Operator.A_CHARCONST:
            AstNode.raise_error(
                "Semantic Error: MINUS operator is not allowed for character constants")
        p.constant[1] = "-"+p.constant[1]
        head = AstNode(Operator.A_CASESINGLE,
                       left=p.constant, right=p.statements)
        p.statements.parent = head
        return head

    # @_('CASE LPAREN neg_int_constant RPAREN COLON scope_open statements scope_close')
    # def case_statement(self, p):
    #     #print("P constant", p.constant[0])
    #     if p.neg_int_constant[0] != Operator.A_INTCONST and p.neg_int_constant[0] != Operator.A_CHARCONST:
    #         Parser.error("Case statement variable must be of type int or char")
    #     head = AstNode(Operator.A_CASESINGLE,
    #                    left=p.neg_int_constant, right=p.statements)
    #     p.statements.parent = head
    #     return head

    # @_('CASE LPAREN neg_float_constant RPAREN COLON scope_open statements scope_close')
    # def case_statement(self, p):
    #     #print("P constant", p.constant[0])
    #     if p.neg_float_constant[0] != Operator.A_INTCONST and p.neg_float_constant[0] != Operator.A_CHARCONST:
    #         Parser.error("Case statement variable must be of type int or char")
    #     head = AstNode(Operator.A_CASESINGLE,
    #                    left=p.neg_float_constant, right=p.statements)
    #     p.statements.parent = head
    #     return head

    # default_statement -> DEFAULT COLON statements
    @_('DEFAULT COLON scope_open statements scope_close')
    def default_statement(self, p):
        head = AstNode(Operator.A_DEFAULT, left=p.statements)
        p.statements.parent = head
        return head

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
        return AstNode(Operator.A_INPUT, left=p.left_value)
        # return str(p[0]+p[1]+p[2]+p[3])

    # output_statement -> OUTPUT ( left_value )  | OUTPUT ( constant )
    @_('OUTPUT LPAREN left_value RPAREN')
    def output_statement(self, p):
        return AstNode(Operator.A_OUTPUT, left=p.left_value)

    @_('OUTPUT LPAREN constant RPAREN')
    def output_statement(self, p):
        return AstNode(Operator.A_OUTPUT, left=p.constant)

    @_('OUTPUT LPAREN MINUS constant RPAREN')
    def output_statement(self, p):
        # semantic check here to not allow negative strings and chars
        if p.constant[0] == Operator.A_CHARCONST or p.constant[0] == Operator.A_STRINGCONST or p.constant[0] == Operator.A_BOOLCONST:
            AstNode.raise_error(
                "Semantic Error: MINUS operator is not allowed for strings, chars and boolean values")
        p.constant[1] = "-"+p.constant[1]
        return AstNode(Operator.A_OUTPUT, left=p.constant)

    # @_('OUTPUT LPAREN neg_int_constant RPAREN')
    # def output_statement(self, p):
    #     return AstNode(Operator.A_OUTPUT, left=p.neg_int_constant)

    # @_('OUTPUT LPAREN neg_float_constant RPAREN')
    # def output_statement(self, p):
    #     return AstNode(Operator.A_OUTPUT, left=p.neg_float_constant)

    # jump_statement -> BREAK | return_statement
    @_('BREAK')
    def jump_statement(self, p):
        return AstNode(Operator.A_BREAK, value=p.BREAK)

    @_('return_statement')
    def jump_statement(self, p):
        return p.return_statement

    @_('CONTINUE')
    def jump_statement(self, p):
        return AstNode(Operator.A_CONTINUE, value=p.CONTINUE)

    # return_statement -> RETURN expr | RETURN
    @_('RETURN expr')
    def return_statement(self, p):
        return AstNode(Operator.A_RETURN, left=p.expr)
        # return str('return ' + p.expr)

    @_('RETURN')
    def return_statement(self, p):
        return AstNode(Operator.A_RETURN)

    @_('expr PLUS expr')
    def expr(self, p):
        data_type = self.type_checker.return_datatype(
            left_type=p.expr0.data_type, right_type=p.expr1.data_type, operator=Operator.A_PLUS)
        return AstNode(Operator.A_PLUS, left=p.expr0, right=p.expr1, data_type=data_type)

    @_('expr MINUS expr')
    def expr(self, p):
        data_type = self.type_checker.return_datatype(
            left_type=p.expr0.data_type, right_type=p.expr1.data_type, operator=Operator.A_MINUS)
        return AstNode(Operator.A_MINUS, left=p.expr0, right=p.expr1, data_type=data_type)

    @_('expr MULT expr')
    def expr(self, p):
        data_type = self.type_checker.return_datatype(
            left_type=p.expr0.data_type, right_type=p.expr1.data_type, operator=Operator.A_MULTIPLY)
        return AstNode(Operator.A_MULTIPLY, left=p.expr0, right=p.expr1, data_type=data_type)

    @_('expr DIVIDE expr')
    def expr(self, p):
        data_type = self.type_checker.return_datatype(
            left_type=p.expr0.data_type, right_type=p.expr1.data_type, operator=Operator.A_DIVIDE)
        return AstNode(Operator.A_DIVIDE, left=p.expr0, right=p.expr1, data_type=data_type)

    @_('expr MOD expr')
    def expr(self, p):
        data_type = self.type_checker.return_datatype(
            left_type=p.expr0.data_type, right_type=p.expr1.data_type, operator=Operator.A_MODULO)
        return AstNode(Operator.A_MODULO, left=p.expr0, right=p.expr1, data_type=data_type)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        #print("UNary check")

        data_type = self.type_checker.return_datatype(
            left_type=p.expr.data_type, operator=Operator.A_NEGATE)
        return AstNode(Operator.A_NEGATE, left=p.expr, data_type=data_type)

    @_('LPAREN expr RPAREN %prec PAREN')
    def expr(self, p):
        return p.expr

    @_('expr RELOP1 expr')
    def expr(self, p):
        data_type = self.type_checker.return_datatype(
            left_type=p.expr0.data_type, right_type=p.expr1.data_type, operator=Operator.A_RELOP1)
        return AstNode(Operator.A_RELOP1, left=p.expr0, right=p.expr1, value=p.RELOP1, data_type=data_type)

    @_('expr RELOP2 expr')
    def expr(self, p):
        data_type = self.type_checker.return_datatype(
            left_type=p.expr0.data_type, right_type=p.expr1.data_type, operator=Operator.A_RELOP2)
        return AstNode(Operator.A_RELOP2, left=p.expr0, right=p.expr1, value=p.RELOP2, data_type=data_type)

    @_('expr AND expr')
    def expr(self, p):
        # print('first',p.expr0.data_type,'second',p.expr1.data_type)
        data_type = self.type_checker.return_datatype(
            left_type=p.expr0.data_type, right_type=p.expr1.data_type, operator=Operator.A_AND)
        return AstNode(Operator.A_AND, left=p.expr0, right=p.expr1, data_type=data_type)

    @_('expr OR expr')
    def expr(self, p):
        data_type = self.type_checker.return_datatype(
            left_type=p.expr0.data_type, right_type=p.expr1.data_type, operator=Operator.A_OR)
        return AstNode(Operator.A_OR, left=p.expr0, right=p.expr1, data_type=data_type)

    @_('NOT expr')
    def expr(self, p):
        data_type = self.type_checker.return_datatype(
            left_type=p.expr.data_type, operator=Operator.A_NOT)
        return AstNode(Operator.A_NOT, left=p.expr, data_type=data_type)

    @_('VARNAME')
    def expr(self, p):
        data_type = self.get_data_type(p.VARNAME)
        self.check_if_variable(p.VARNAME)
        return AstNode(Operator.A_VARIABLE, value=p.VARNAME, data_type=data_type)

    @_('array_var_use')
    def expr(self, p):
        return AstNode(Operator.A_ARREXPR_VARIABLE, left=p.array_var_use, data_type=p.array_var_use.data_type)

    # expr -> constant
    @_('constant')
    def expr(self, p):
        #print("The const type", p.constant[0])
        data_type = self.type_checker.return_datatype(operator=p.constant[0])
        # p.constant = [Operator.A_CHARCONST, 't'] for a character
        return AstNode(p.constant[0], value=p.constant[1], data_type=data_type)

    # @_('neg_int_constant')
    # def expr(self, p):
    #     #print("The const type", p.constant[0])
    #     data_type = self.type_checker.return_datatype(
    #         operator=p.neg_int_constant[0])
    #     # p.constant = [Operator.A_CHARCONST, 't'] for a character
    #     return AstNode(p.neg_int_constant[0], value=p.neg_int_constant[1], data_type=data_type)

    # @_('neg_float_constant')
    # def expr(self, p):
    #     #print("The const type", p.constant[0])
    #     data_type = self.type_checker.return_datatype(
    #         operator=p.neg_float_constant[0])
    #     # p.constant = [Operator.A_CHARCONST, 't'] for a character
    #     return AstNode(p.neg_float_constant[0], value=p.neg_float_constant[1], data_type=data_type)

    # expr -> (DATATYPE) expr#
    @_('LPAREN DATATYPE RPAREN expr %prec TYPECASTING')
    def expr(self, p):
        data_type = self.type_checker.return_datatype(
            left_type=p.DATATYPE, right_type=p.expr.data_type, operator=Operator.A_TYPECAST)
        return AstNode(Operator.A_TYPECAST, left=p.DATATYPE, right=p.expr, data_type=data_type)

    # assignment_statement -> left_value = expr
    @_('left_value ASSIGN expr')
    def assignment_statement(self, p):
        return AstNode(Operator.A_ASSIGN_STMT, left=p.left_value, right=p.expr, data_type=p.left_value.data_type)

    # left_value -> VARNAME | array_variable
    @_('VARNAME')
    def left_value(self, p):
        data_type = self.get_data_type(p.VARNAME)
        self.check_if_variable(p.VARNAME)

        return AstNode(Operator.A_VARIABLE, value=p.VARNAME, data_type=data_type)

    @_('array_var_use')
    def left_value(self, p):
        return AstNode(Operator.A_ARREXPR_VARIABLE, left=p.array_var_use)

    # constant -> INTVAL | FLOATVAL | CHARVAL | STRINGVAL | BOOLVAL
    @_('INTVAL')
    def constant(self, p):
        # return AstNode(Operator.A_INTCONST, value=p.INTVAL)
        return [Operator.A_INTCONST, p.INTVAL]

    # @_('MINUS INTVAL')
    # def neg_int_constant(self, p):
    #     # return AstNode(Operator.A_INTCONST, value=p.INTVAL)
    #     print("minus here")
    #     return [Operator.A_INTCONST, "-"+str(p.INTVAL)]

    @_('FLOATVAL')
    def constant(self, p):
        return [Operator.A_FLOATCONST, p.FLOATVAL]

    # @_('MINUS FLOATVAL')
    # def neg_float_constant(self, p):
    #     return [Operator.A_FLOATCONST, "-"+str(p.FLOATVAL)]

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
        return p.function_call
        # return str(p.function_call)

    # function_call -> VARNAME ( argument_list )
    @_('VARNAME LPAREN argument_list RPAREN')
    def function_call(self, p):
        # here "p.argument_list" could be "None", if there are no arguments
        # ----- semantic check --------
        args_types = []
        cur = p.argument_list
        while cur.operator == Operator.A_NODE:
            data_type = cur.left.data_type
            args_types.append(data_type)
            cur = cur.right
        args_types.append(cur.data_type)

        # print("LOOK HERE : ", parameters)

        self.check_function_signature(p.VARNAME, args_types)

        # -----------------------
        head = AstNode(Operator.A_FUNCCALL, left=p.VARNAME,
                       right=p.argument_list)
        return head

    # argument_list -> argument_list_rec | e
    @_('argument_list_rec')
    def argument_list(self, p):
        return p.argument_list_rec

    @_('empty')
    def argument_list(self, p):
        return None

    @_('expr COMMA argument_list_rec')
    def argument_list_rec(self, p):
        head = AstNode(Operator.A_NODE, left=p.expr, right=p.argument_list_rec)
        return head

    @_('expr')
    def argument_list_rec(self, p):
        return p.expr

    # argument -> VARNAME | constant | array_variable
    # @_('VARNAME',
        # 'constant',
        # 'array_variable')
    # def argument(self, p):
        # return str(p[0])

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

    with open(os.path.join(TEST_SUITES_DIR, "LiveDemoTest5.sq"), 'r') as f:
        text = f.read()

    parser.parse(lex.tokenize(text))
