from typing import Type

from click import pass_obj
from SemanticAnalysis import TypeChecker
from enum import Enum
import math

INT = "int"
FLOAT = "float"
STRING = "string"
BOOL = "bool"
CHAR = "char"


class Operator(Enum):
    A_AND = "&&"
    A_OR = "||"
    A_EQUAL = "=="
    A_NOT_EQUAL = "!="
    A_LESS_THAN = "<"
    A_GREATER_THAN = ">"
    A_LESS_THAN_EQUAL = "<="
    A_GREATER_THAN_EQUAL = ">="
    A_RELOP1 = '<|>|<=|>='
    A_RELOP2 = '==|!='
    A_PLUS = "+"
    A_MINUS = "-"
    A_MULTIPLY = "*"
    A_DIVIDE = "/"
    A_MODULO = "%"
    A_NOT = "!"
    A_NEGATE = "uminus"
    A_TYPECAST = "type cast"
    A_ASSIGN = "="
    A_IF = "if"
    A_ELSE = "else"
    A_WHILE = "while"
    A_FOR = "for"
    A_RETURN = "return"
    A_BREAK = "break"
    A_VARIABLE = "var"
    A_BOOLCONST = "bool const"
    A_INTCONST = "int const"
    A_FLOATCONST = "float const"
    A_STRINGCONST = "string const"
    A_CHARCONST = "char const"
    A_ARR_LITERAL = "arr literal"
    A_FUNC = "func"
    A_FUNCCALL = "func call"
    A_NODE = "node"
    A_ROOT = "root"
    A_DECL = "decl"
    A_ARR_DECL = "array_decl"
    A_IFELSE = "if else"
    A_CONTINUE = "continue"
    A_IFELIF = "if elif"
    A_ELIFSINGLE = "elif single"
    A_ELIFMULTIPLE = "elif multiple"
    A_IFELIFELSE = "if elif else"
    A_ASSIGN_STMT = "assign stmt"
    A_SWITCH = "switch"
    A_CASESINGLE = "case single"
    A_CASEMULTIPLE = "case multiple"
    A_DEFAULT = "case default"
    A_SWITCHPARENT = "switch parent"
    A_IFPARENT = "if parent"
    A_FORPARENT = "for parent"
    A_BOOL = "bool"
    A_ARRAY_REC = "array rec"
    A_ARRAY_VARIABLE_REC = "array variable rec"
    A_ARRAY_VARIABLE = "array variable"
    A_ARREXPR_VARIABLE = "array expr variable"
    A_ARR_EXPR_REC = "array expr rec"


#typeChecker = TypeChecker.TypeChecker()


class AstNode:
    '''
    If a node contains 2 children, they must be assigned to the left and right attributes
    If a node contains 1 child, it must be assigned to the left child
    '''

    def __init__(self, operator=None, left=None, mid=None, right=None,
                 value=None, data_type='fuzzy', next_label=None):
        self.operator = operator
        self.left = left
        self.mid = mid
        self.right = right
        self.value = value
        # undefined datatype is called 'fuzzy', default initialization
        self.data_type = data_type
        self.true = None
        self.false = None
        self.code = None
        self.next = next_label

        #print("Value", self.value, "Datatype", self.data_type)
        # self.parent = parent

    @staticmethod
    def generateCode(head, parser):

        if head is None:
            return

        # --------------------------------------------------

        if head.operator == Operator.A_ROOT:

            left = head.left
            #typeChecker.check(head, parser.symbol_table)
            AstNode.generateCode(left, parser)
            # head.code = left.code + '\n' + left.next + ':\n'
            head.code = left.code

            # TODO: place this output file in the Output folder and rename the file
            with open("output.tac", "w") as f:
                f.write(head.code)

        # --------------------------------------------------

        elif head.operator == Operator.A_NODE:
            # print(head.operator.value + " ?")

            left, right = head.left, head.right

            if left and right:
                right.next = parser.get_new_label()
                left.next = parser.get_new_label()
                AstNode.generateCode(left, parser)
                AstNode.generateCode(right, parser)
                # if head.value == "for":
                #     head.code = left.code + '\n' + right.code
                # else:
                head.code = left.code + '\n' + right.code + "\n" + right.next + ':'

            elif left:
                left.next = parser.get_new_label()
                AstNode.generateCode(left, parser)
                head.code = left.code + '\n' + left.next + ':\n'

            return

        # ------------------------------------------------------------

        elif head.operator == Operator.A_FUNC:
            params, statements = head.left, head.right
            # function_name is same as the label
            function_name = head.value

            AstNode.generateCode(statements, parser)

            # head.code = statements.code + "\n" + head.next + ":\n" + "return\n"
            head.code = function_name + ":\n" + statements.code + "\n"

        # ------------------------------------------------------------

        elif head.operator == Operator.A_AND:
            # TODO: Ask Kranthi aboutthis and add TAC for type casting

            left, right = head.left, head.right
            true, false = head.true, head.false

            if left.operator == Operator.A_VARIABLE:
                left = AstNode(Operator.A_BOOL, left=left)

            if right.operator == Operator.A_VARIABLE:
                right = AstNode(Operator.A_BOOL, left=right)

            left.true = parser.get_new_label()
            left.false = false
            right.true = true
            right.false = false

            AstNode.generateCode(left, parser)
            AstNode.generateCode(right, parser)

            # if not left.value:
            #     left.code = f"left.value == true"

            head.code = left.code + "\n" + left.true + ":" + "\n" + right.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_OR:
            # TODO: Ask Kranthi aboutthis and add TAC for type casting

            left, right = head.left, head.right
            true, false = head.true, head.false

            if left.operator == Operator.A_VARIABLE:
                left = AstNode(Operator.A_BOOL, left=left)

            if right.operator == Operator.A_VARIABLE:
                right = AstNode(Operator.A_BOOL, left=right)

            left.true = true
            left.false = parser.get_new_label()
            right.true = true
            right.false = false

            AstNode.generateCode(left, parser)
            AstNode.generateCode(right, parser)

            head.code = left.code + "\n" + left.false + ":" + "\n" + right.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_RELOP1 or head.operator == Operator.A_RELOP2:

            left, right = head.left, head.right
            left_type = left.data_type
            right_type = right.data_type
            relop = head.value

            AstNode.generateCode(left, parser)
            AstNode.generateCode(right, parser)

            head.code = left.code + "\n" + right.code + "\n"

            """ head.code += f"if {left.value} {relop} {right.value} goto {head.true}\ngoto {head.false}\n"
            "if " + left.value + " " + relop + " " + right.value + " goto " + head.true + "\n" + "goto " + head.false """

            if left_type == 'int' and right_type == 'int':
                head.code += f"if {left.value} {relop} {right.value} goto {head.true}\ngoto {head.false}\n"
            elif left_type == 'float' and right_type == 'float':
                pass
            elif left_type == 'float' or right_type == 'float':
                if left_type == 'float':
                    typecast_variable = parser.get_new_temp("float")
                    head.code += f"{typecast_variable} = (float){right.value}\n"
                    head.code += f"if {left.value} {relop} {typecast_variable} goto {head.true}\ngoto {head.false}\n"
                else:
                    typecast_variable = parser.get_new_temp("float")
                    head.code += f"{typecast_variable} = (float){left.value}\n"
                    head.code += f"if {typecast_variable} {relop} {right.value} goto {head.true}\ngoto {head.false}\n"

            else:
                typecast_variable_left = left.value
                typecast_variable_right = right.value
                if left_type != 'int':
                    typecast_variable_left = parser.get_new_temp("int")
                    head.code += f"{typecast_variable_left} = (int){left.value}\n"
                if right_type != 'int':
                    typecast_variable_right = parser.get_new_temp("int")
                    head.code += f"{typecast_variable_right} = (int){right.value}\n"
                head.code += f"if {typecast_variable_left} {relop} {typecast_variable_right} goto {head.true}\ngoto {head.false}\n"

        # ------------------------------------------------------------

        elif head.operator == Operator.A_NOT:

            left = head.left
            true, false = head.true, head.false

            if left.operator == Operator.A_VARIABLE:
                left = AstNode(Operator.A_BOOL, left=left)

            left.true = false
            left.false = true

            AstNode.generateCode(left, parser)

            head.code = left.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_IF or head.operator == Operator.A_ELIFSINGLE:
            expr, statements = head.left, head.right

            if expr.operator == Operator.A_VARIABLE or expr.operator == Operator.A_INTCONST:
                expr = AstNode(Operator.A_BOOL, left=expr)

            elif expr.operator == Operator.A_FLOATCONST or expr.operator == Operator.A_STRINGCONST:
                expr = AstNode(Operator.A_BOOL, left=expr)

            elif expr.operator == Operator.A_CHARCONST:
                expr = AstNode(Operator.A_BOOL, left=expr)

            elif expr.operator == Operator.A_PLUS or expr.operator == Operator.A_MINUS or \
                    expr.operator == Operator.A_MULTIPLY or expr.operator == Operator.A_DIVIDE or \
                    expr.operator == Operator.A_MODULO:
                expr = AstNode(Operator.A_BOOL, left=expr)

            expr.true = parser.get_new_label()
            expr.false = head.next
            statements.next = head.next

            AstNode.generateCode(expr, parser)
            AstNode.generateCode(statements, parser)

            head.code = expr.code + "\n" + expr.true + ":\n" + statements.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_IFELSE or head.operator == Operator.A_ELIFMULTIPLE or head.operator == Operator.A_IFELIFELSE:

            expr, statements1, statements2 = head.left, head.mid, head.right

            if expr.operator == Operator.A_VARIABLE or expr.operator == Operator.A_INTCONST:
                expr = AstNode(Operator.A_BOOL, left=expr)

            elif expr.operator == Operator.A_FLOATCONST or expr.operator == Operator.A_STRINGCONST:
                expr = AstNode(Operator.A_BOOL, left=expr)

            elif expr.operator == Operator.A_CHARCONST:
                expr = AstNode(Operator.A_BOOL, left=expr)

            elif expr.operator == Operator.A_PLUS or expr.operator == Operator.A_MINUS or \
                    expr.operator == Operator.A_MULTIPLY or expr.operator == Operator.A_DIVIDE or \
                    expr.operator == Operator.A_MODULO:
                expr = AstNode(Operator.A_BOOL, left=expr)

            expr.true = parser.get_new_label()
            expr.false = parser.get_new_label()
            statements1.next = head.next
            statements2.next = head.next

            AstNode.generateCode(expr, parser)
            AstNode.generateCode(statements1, parser)
            AstNode.generateCode(statements2, parser)

            head.code = expr.code + "\n" + expr.true + ":\n" + statements1.code + "\n" + \
                "goto " + head.next + "\n" + expr.false + ":\n" + statements2.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_SWITCHPARENT or head.operator == Operator.A_IFPARENT or head.operator == Operator.A_FORPARENT:

            print(head.operator.value + " ?")
            left = head.left

            head.next = parser.get_new_label()
            left.next = head.next

            AstNode.generateCode(left, parser)

            head.code = left.code + '\n'
            # print('aaaaa', head.code)

        # ------------------------------------------------------------

        elif head.operator == Operator.A_SWITCH:

            left, right = head.left, head.right

            head.value = left
            right.value = head.value
            right.next = head.next
            print('a_switch', right.next)

            AstNode.generateCode(right, parser)

            head.code = right.code
            # print('abc', right.code)

        # ------------------------------------------------------------

        elif head.operator == Operator.A_CASEMULTIPLE:

            single, multiple = head.left, head.right

            multiple.next = head.next
            multiple.value = head.value
            single.value = head.value
            single.next = head.next

            AstNode.generateCode(single, parser)
            AstNode.generateCode(multiple, parser)

            head.code = single.code + "\n" + multiple.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_CASESINGLE:

            constant, statements = head.left, head.right

            statements.next = parser.get_new_label()

            AstNode.generateCode(statements, parser)

            head.code = "ifFalse " + head.value + " == " + constant[1] + " goto " + statements.next + \
                statements.code + "\n" + "goto " + head.next + "\n" + statements.next + ":\n"
            print('abc', statements.code)

        # ------------------------------------------------------------

        elif head.operator == Operator.A_DEFAULT:

            statements = head.left

            statements.next = head.next

            AstNode.generateCode(statements, parser)

            head.code = statements.code + "\n" + "goto " + head.next

        # ------------------------------------------------------------

        elif head.operator == Operator.A_WHILE:

            expr, statements = head.left, head.right

            if expr.operator == Operator.A_VARIABLE or expr.operator == Operator.A_INTCONST:
                expr = AstNode(Operator.A_BOOL, left=expr)

            elif expr.operator == Operator.A_FLOATCONST or expr.operator == Operator.A_STRINGCONST:
                expr = AstNode(Operator.A_BOOL, left=expr)

            elif expr.operator == Operator.A_CHARCONST:
                expr = AstNode(Operator.A_BOOL, left=expr)

            elif expr.operator == Operator.A_PLUS or expr.operator == Operator.A_MINUS or \
                    expr.operator == Operator.A_MULTIPLY or expr.operator == Operator.A_DIVIDE or \
                    expr.operator == Operator.A_MODULO:
                expr = AstNode(Operator.A_BOOL, left=expr)

            head.begin = parser.get_new_label()
            expr.true = parser.get_new_label()
            expr.false = head.next
            statements.next = head.begin

            AstNode.generateCode(expr, parser)
            AstNode.generateCode(statements, parser)

            head.code = head.begin + ":\n" + expr.code + "\n" + expr.true + ":\n" + statements.code + "\n" + \
                "goto " + head.begin

        # ------------------------------------------------------------

        elif head.operator == Operator.A_FOR:

            left, mid, right = head.left, head.mid, head.right

            if left.operator == Operator.A_VARIABLE or left.operator == Operator.A_INTCONST:
                left = AstNode(Operator.A_BOOL, left=left)

            elif left.operator == Operator.A_FLOATCONST or left.operator == Operator.A_STRINGCONST:
                left = AstNode(Operator.A_BOOL, left=left)

            elif left.operator == Operator.A_CHARCONST:
                left = AstNode(Operator.A_BOOL, left=left)

            elif left.operator == Operator.A_PLUS or left.operator == Operator.A_MINUS or \
                    left.operator == Operator.A_MULTIPLY or left.operator == Operator.A_DIVIDE or \
                    left.operator == Operator.A_MODULO:
                left = AstNode(Operator.A_BOOL, left=left)

            # new instance variable created for the "A_FOR" node
            # setattr(head, 'begin', parser.get_new_label())
            head.begin = parser.get_new_label()
            left.true = parser.get_new_label()
            left.false = head.next
            mid.next = head.begin

            AstNode.generateCode(left, parser)
            AstNode.generateCode(mid, parser)
            AstNode.generateCode(right, parser)
            head.code = head.begin + ":\n" + left.code + "\n" + left.true + ":\n" + right.code + "\n" + \
                mid.code + "\n" + "goto " + head.begin

        # ------------------------------------------------------------

        elif head.operator == Operator.A_PLUS:

            expr0, expr1 = head.left, head.right

            AstNode.generateCode(expr0, parser)
            AstNode.generateCode(expr1, parser)

            head.value = parser.get_new_temp(head.data_type)

            # head.code = expr0.code + "\n" + expr1.code + "\n" + \
            # head.value + " = " + expr0.value + " + " + expr1.value

            head.code = expr0.code + "\n" + expr1.code + "\n"

            if head.data_type != expr0.data_type:
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{typecast_variable} = ({head.data_type}){expr0.value}\n"
                head.code += f"{head.value} = {typecast_variable} + {expr1.value}\n"

            elif head.data_type != expr1.data_type:
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{parser.get_new_temp(head.data_type)} = ({head.data_type}){expr1.value}\n"
                head.code += f"{head.value} = {expr0.value} + {typecast_variable}\n"
            else:
                head.code += f"{head.value} = {expr0.value} + {expr1.value}\n"

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_MINUS or head.operator == Operator.A_NEGATE:

            expr0, expr1 = head.left, head.right

            if(expr1 == None):
                head.value = parser.get_new_temp(head.data_type)

                AstNode.generateCode(expr0, parser)

                # head.code = expr0.code + "\n" +  \
                #     head.value + " = " + " - " + expr0.value
                head.code = expr0.code + "\n"

                if head.data_type != expr0.data_type:
                    typecast_variable = parser.get_new_temp(head.data_type)
                    head.code += f"{typecast_variable} = ({head.data_type}) - {expr0.value}\n"
                else:
                    head.code += f"{head.value} = - {expr0.value}\n"

            else:
                head.value = parser.get_new_temp(head.data_type)

                AstNode.generateCode(expr0, parser)
                AstNode.generateCode(expr1, parser)

                # head.code = expr0.code + "\n" + expr1.code + "\n" + \
                # head.value + " = " + expr0.value + " - " + expr1.value
                head.code = expr0.code + "\n" + expr1.code + "\n"

                if head.data_type != expr0.data_type:
                    typecast_variable = parser.get_new_temp(head.data_type)
                    head.code += f"{typecast_variable} = ({head.data_type}){expr0.value}\n"
                    head.code += f"{head.value} = {typecast_variable} - {expr1.value}\n"

                elif head.data_type != expr1.data_type:
                    typecast_variable = parser.get_new_temp(head.data_type)
                    head.code += f"{parser.get_new_temp(head.data_type)} = ({head.data_type}){expr1.value}\n"
                    head.code += f"{head.value} = {expr0.value} - {typecast_variable}\n"
                else:
                    head.code += f"{head.value} = {expr0.value} - {expr1.value}\n"

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_MULTIPLY:

            expr0, expr1 = head.left, head.right

            head.value = parser.get_new_temp(head.data_type)

            AstNode.generateCode(expr0, parser)
            AstNode.generateCode(expr1, parser)

            # head.code = expr0.code + "\n" + expr1.code + "\n" + \
            # head.value + " = " + expr0.value + " * " + expr1.value
            head.code = expr0.code + "\n" + expr1.code + "\n"

            if head.data_type != expr0.data_type:
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{typecast_variable} = ({head.data_type}){expr0.value}\n"
                head.code += f"{head.value} = {typecast_variable} * {expr1.value}\n"

            elif head.data_type != expr1.data_type:
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{parser.get_new_temp(head.data_type)} = ({head.data_type}){expr1.value}\n"
                head.code += f"{head.value} = {expr0.value} * {typecast_variable}\n"
            else:
                head.code += f"{head.value} = {expr0.value} * {expr1.value}\n"

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_DIVIDE:

            expr0, expr1 = head.left, head.right

            head.value = parser.get_new_temp(head.data_type)

            AstNode.generateCode(expr0, parser)
            AstNode.generateCode(expr1, parser)

            # head.code = expr0.code + "\n" + expr1.code + "\n" + \
            # head.value + " = " + expr0.value + " / " + expr1.value

            print('1', expr0.code, '2', expr1.code)
            head.code = expr0.code + "\n" + expr1.code + "\n"

            if head.data_type != expr0.data_type:
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{typecast_variable} = ({head.data_type}){expr0.value}\n"
                head.code += f"{head.value} = {typecast_variable} / {expr1.value}\n"

            elif head.data_type != expr1.data_type:
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{parser.get_new_temp(head.data_type)} = ({head.data_type}){expr1.value}\n"
                head.code += f"{head.value} = {expr0.value} / {typecast_variable}\n"
            else:
                head.code += f"{head.value} = {expr0.value} / {expr1.value}\n"
        # --------------------------------------------------------------------

        elif head.operator == Operator.A_MODULO:

            expr0, expr1 = head.left, head.right

            head.value = parser.get_new_temp(head.data_type)

            AstNode.generateCode(expr0, parser)
            AstNode.generateCode(expr1, parser)

            head.code = expr0.code + "\n" + expr1.code + "\n" + \
                head.value + " = " + expr0.value + " % " + expr1.value

        # --------------------------------------------------------------------

        # semantic analysis is required here

        elif head.operator == Operator.A_ARREXPR_VARIABLE:

            array_variable = head.left

            AstNode.generateCode(array_variable, parser)

            variable = list(filter(
                lambda var: var["scope"] == array_variable.value["scope"] and var["identifier_name"] == array_variable.value["varname"],
                parser.symbol_table
            ))
            data_type = variable[0]["type"]

            temp = parser.get_new_temp(data_type)

            if data_type == INT:
                size = 4
            elif data_type == CHAR:
                size = 1
            elif data_type == FLOAT:
                size = 4
            elif data_type == BOOL:
                size = 1

            head.value = array_variable.value["varname"] + "[" + temp + "]"
            head.code = array_variable.code + "\n" + \
                temp + " = " + array_variable.value["val"] + " * " + str(size)

        # --------------------------------------------------------------------

        # semantic analysis is required here

        elif head.operator == Operator.A_ARR_EXPR_REC:

            if head.right is not None:
                array_var_use, expr = head.left, head.right

                AstNode.generateCode(array_var_use, parser)
                AstNode.generateCode(expr, parser)

                temp = parser.get_new_temp(head.data_type)
                # TODO : check if this is fine
                head.value["val"] = parser.get_new_temp(head.data_type)

                # print("eye catchy : " , head.data_type)

                index = head.value["index"]
                variable = list(filter(
                    lambda var: var["scope"] == head.value["scope"] and var["identifier_name"] == head.value["varname"],
                    parser.symbol_table
                ))
                i = index
                dimension = 1
                for j in range(i, len(variable[0]["dimension"])):
                    dimension *= variable[0]["dimension"][j]

                head.code = array_var_use.code + "\n" + expr.code + "\n" + temp + " = " + expr.value + " * " + str(dimension) + "\n" + \
                    head.value["val"] + " = " + \
                    array_var_use.value["val"] + " + " + temp

            else:
                expr = head.left

                AstNode.generateCode(expr, parser)

                index = head.value["index"]
                variable = list(filter(
                    lambda var: var["scope"] == head.value["scope"] and var["identifier_name"] == head.value["varname"],
                    parser.symbol_table
                ))
                i = index
                dimension = 1
                for j in range(i, len(variable[0]["dimension"])):
                    dimension *= variable[0]["dimension"][j]

                head.value["val"] = parser.get_new_temp(head.data_type)
                head.code = expr.code + "\n" + \
                    head.value["val"] + " = " + \
                    expr.value + " * " + str(dimension)

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_ASSIGN_STMT:
            # TODO: Code to check types and TAC for implicit/explicit casting

            if type(head.left) == str:
                varname, expr = head.left, head.right

                AstNode.generateCode(expr, parser)
                head.code = expr.code + "\n" + varname + " = " + expr.value

            else:
                left_value, expr = head.left, head.right

                AstNode.generateCode(left_value, parser)
                AstNode.generateCode(expr, parser)

                head.code = left_value.code + "\n" + expr.code + \
                    "\n" + left_value.value + " = " + expr.value

            return

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_DECL:

            left = head.left

            # to distinguish between init and declaration
            if head.right is not None:
                # initialization
                right = head.right

                AstNode.generateCode(right, parser)

                head.code = right.code + "\n" + \
                    left[0] + " " + left[1] + " = " + right.value + "\n"

            else:
                # declaration
                head.code = left[0] + " " + left[1] + " = "
                if left[0] == INT:
                    head.code += "0"
                elif left[0] == FLOAT:
                    head.code += "0.0"
                elif left[0] == STRING:
                    head.code += "\"\""
                elif left[0] == BOOL:
                    head.code += "false"
                elif left[0] == CHAR:
                    head.code += "'0'"

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_ARR_DECL:

            array_rec, array_list = head.left, head.right

            AstNode.generateCode(array_list, parser)

            size = 0
            if head.data_type == INT:
                size = 4
            elif head.data_type == CHAR:
                size = 1
            elif head.data_type == FLOAT:
                size = 4
            elif head.data_type == BOOL:
                size = 1

            head.code = f"{head.data_type} {head.value}[{int(math.prod(array_rec.value['list']))*size}]\n"

            for i in range(len(array_list.value)):
                head.code += f"{head.value}[{i*size}]={array_list.value[i]}\n"

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_ARR_LITERAL:

            left, right = head.left, head.right

            if right == None:
                head.value = [left[1]]
                head.code = ""

            else:
                AstNode.generateCode(left, parser)
                head.value = [*left.value, right[1]]
                head.code = ""

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_BOOLCONST:

            if head.value == "switch" or head.true == None or head.false == None:
                head.code = ""
            else:
                if head.value == "true":
                    head.code = "goto " + head.true
                elif head.value == "false":
                    head.code = "goto " + head.false

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_VARIABLE or head.operator == Operator.A_INTCONST or head.operator == Operator.A_STRINGCONST or head.operator == Operator.A_CHARCONST or head.operator == Operator.A_FLOATCONST:

            head.code = ""

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_BOOL:

            print('unique here')
            left = head.left

            AstNode.generateCode(left, parser)
            # TODO: I dont think is required
            # left variable type is assumed to be "int" or "float"
            # for other types we need to generate code accordingly after semantic analysis
            # for bool : a == true
            # for char : a != '\0'
            # for string : a != ""

            rhs = "0"
            if left.operator == Operator.A_VARIABLE or left.operator == Operator.A_PLUS or left.operator == Operator.A_MINUS or \
                    left.operator == Operator.A_MULTIPLY or left.operator == Operator.A_DIVIDE or \
                    left.operator == Operator.A_MODULO:
                """ if left.data_type == "int":
                    rhs = "0"
                #elif left.data_type == "float":
                   # rhs = "0.0"
                elif left.data_type == "char":
                    rhs = "\\0"
                elif left.data_type == "bool":
                    rhs = "false"
                else:
                    rhs = "false" """

                head.code = left.code + "\n" + \
                    "if " + left.value + " " + "!=" + " " + rhs + " goto " + head.true + \
                    "\n" + "goto " + head.false
            else:
                if left.operator == Operator.A_INTCONST and left.value == "0":
                    head.code = "goto " + head.false
                elif left.operator == Operator.A_STRINGCONST and left.value == "":
                    head.code = "goto " + head.false
                elif left.operator == Operator.A_CHARCONST and left.value == "'\\0'":
                    head.code = "goto " + head.false
                elif left.operator == Operator.A_FLOATCONST and left.value == "0.0":
                    head.code = "goto " + head.false
                else:
                    head.code = "goto " + head.true

        # ---------------------------------------------------------------------------------

        elif head.operator == Operator.A_BREAK:
            cur = head
            # TODO: do this for "while", "switch", if it goes upto ROOT then semantic error
            while(cur.operator != Operator.A_FOR and
                    cur.operator != Operator.A_WHILE and
                    cur.operator != Operator.A_SWITCH
                  ):
                if cur.operator != Operator.A_ROOT:
                    cur = cur.parent
                else:
                    raise Exception(
                        "Semantic Error : \"break\" can only be used in a for_loop or a while_loop or a switch_case.\n")

            head.code = "goto " + cur.next

        elif head.operator == Operator.A_RETURN:

            left = head.left

            if left:
                AstNode.generateCode(left, parser)

                head.code = left.code + '\n' + 'return ' + left.value
            else:
                head.code = 'return'

        elif head.operator == Operator.A_CONTINUE:
            cur = head
            while(cur.operator != Operator.A_FOR and
                    cur.operator != Operator.A_WHILE
                  ):
                if cur.operator != Operator.A_ROOT:
                    cur = cur.parent
                else:
                    raise Exception(
                        "Semantic Error : \"continue\" can only be used in a for_loop or a while_loop.\n")

            head.code = "goto " + cur.begin

        elif head.operator == Operator.A_FUNCCALL:

            function_name = head.left
            argument_list = head.right

            head.value = parser.get_new_temp(head.data_type)

            if argument_list:
                AstNode.generateCode(argument_list, parser)

                args = []
                cur = argument_list
                while cur.operator == Operator.A_NODE:
                    args.append(cur.left.value)
                    cur = cur.right
                args.append(cur.value)

                head.code = argument_list.code + '\n'
                for arg in args:
                    head.code += f"param {arg}\n"
                head.code += f"{head.value} = call {function_name},{len(args)}\n"

            else:
                head.code = f"{head.value} = call {function_name},0\n"

        elif head.operator == Operator.A_TYPECAST:

            data_type = head.left
            expr = head.right

            AstNode.generateCode(expr, parser)

            head.value = parser.get_new_temp(data_type)

            head.code = f"{expr.code}{head.value} = ({data_type}){expr.value}\n"
