# from typing import Type

# from click import pass_obj
# from SemanticAnalysis import TypeChecker
import re
import os
from enum import Enum
import math
import logging as logger
logger.exception = logger.error

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
    A_INPUT = "input"
    A_OUTPUT = "output"
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

default_values = {
    "int": "0",
    "float": "0.0",
    "char": "\'\0\'",
    "string": "\"\"",
    "bool": "false",
    "void": ""
}


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
    def raise_error(message=None):
        try:
            raise Exception(message)
        except Exception as ex:
            logger.exception(ex)
            quit()

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

            return head.code

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
            function_name = head.value["function_name"]

            AstNode.generateCode(statements, parser)

            # head.code = statements.code + "\n" + head.next + ":\n" + "return\n"

            head.code = function_name + ":\n" + statements.code + "\n" + \
                f'return {default_values[head.value["return_type"]]}' + "\n"

        # ------------------------------------------------------------

        elif head.operator == Operator.A_AND:
            left, right = head.left, head.right
            true, false = head.true, head.false

            if true == None or false == None:
                head.value = parser.get_new_temp("int")
                left.true = parser.get_new_label()
                left.false = false
                right.true = true
                right.false = false
                AstNode.generateCode(left, parser)
                AstNode.generateCode(right, parser)
                head.code = left.code + '\n' + right.code
                label1 = parser.get_new_label()
                label2 = parser.get_new_label()
                # print(left.data_type, right.data_type, head.data_type)
                typecast_variable_left = left.value
                typecast_variable_right = right.value
                if left.data_type != 'int':
                    typecast_variable_left = parser.get_new_temp("int")
                    head.code += f"{typecast_variable_left} = (int){left.value}\n"
                if right.data_type != 'int':
                    typecast_variable_right = parser.get_new_temp("int")
                    head.code += f"{typecast_variable_right} = (int){right.value}\n"

                head.code += f"if {typecast_variable_left} == 0 goto {label2}\n"
                head.code += f"if {typecast_variable_right} == 0 goto {label2}\n"
                head.code += f"{head.value} = true\n"
                head.code += f"goto {label1}\n"
                head.code += f"{label2}:\n"
                head.code += f"{head.value} = false\n"
                head.code += f"{label1}:\n"
                return

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
            left, right = head.left, head.right
            true, false = head.true, head.false

            if true == None or false == None:
                head.value = parser.get_new_temp("int")
                left.true = parser.get_new_label()
                left.false = false
                right.true = true
                right.false = false
                AstNode.generateCode(left, parser)
                AstNode.generateCode(right, parser)
                head.code = left.code + '\n' + right.code + "\n"
                label1 = parser.get_new_label()
                label2 = parser.get_new_label()
                typecast_variable_left = left.value
                typecast_variable_right = right.value
                if left.data_type != 'int':
                    typecast_variable_left = parser.get_new_temp("int")
                    head.code += f"{typecast_variable_left} = (int){left.value}\n"
                if right.data_type != 'int':
                    typecast_variable_right = parser.get_new_temp("int")
                    head.code += f"{typecast_variable_right} = (int){right.value}\n"
                head.code += f"if {typecast_variable_left} != 0 goto {label2}\n"
                head.code += f"if {typecast_variable_right} != 0 goto {label2}\n"
                head.code += f"{head.value} = false\n"
                head.code += f"goto {label1}\n"
                head.code += f"{label2}:\n"
                head.code += f"{head.value} = true\n"
                head.code += f"{label1}:\n"
                return

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

            if head.true == None or head.false == None:
                temp = parser.get_new_temp("bool")
                # head.code += f"{temp} = {left.value} {relop} {right.value}"

                if left_type == 'int' and right_type == 'int':
                    head.code += f"{temp} = {left.value} {relop} {right.value}\n"
                elif left_type == 'float' and right_type == 'float':
                    head.code += f"{temp} = {left.value} {relop} {right.value}\n"
                elif left_type == 'float' or right_type == 'float':
                    if left_type == 'float':
                        typecast_variable = parser.get_new_temp("float")
                        head.code += f"{typecast_variable} = (float){right.value}\n"
                        head.code += f"{temp} = {left.value} {relop} {typecast_variable}"
                    else:
                        typecast_variable = parser.get_new_temp("float")
                        head.code += f"{typecast_variable} = (float){left.value}\n"
                        head.code += f"{temp} = {typecast_variable} {relop} {right.value}"

                else:
                    typecast_variable_left = left.value
                    typecast_variable_right = right.value
                    if left_type != 'int':
                        typecast_variable_left = parser.get_new_temp("int")
                        head.code += f"{typecast_variable_left} = (int){left.value}\n"
                    if right_type != 'int':
                        typecast_variable_right = parser.get_new_temp("int")
                        head.code += f"{typecast_variable_right} = (int){right.value}\n"
                    head.code += f"{temp} = {typecast_variable_left} {relop} {typecast_variable_right}"
                head.value = temp
                return

            if left_type == 'int' and right_type == 'int':
                head.code += f"if {left.value} {relop} {right.value} goto {head.true}\ngoto {head.false}\n"
            elif left_type == 'float' and right_type == 'float':
                head.code += f"if {left.value} {relop} {right.value} goto {head.true}\ngoto {head.false}\n"
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

            if true == None or false == None:
                head.value = parser.get_new_temp("int")
                left.true = false
                left.false = true
                AstNode.generateCode(left, parser)
                head.code = left.code + '\n'
                label1 = parser.get_new_label()
                label2 = parser.get_new_label()
                typecast_variable_left = left.value
                if left.data_type != 'int':
                    typecast_variable_left = parser.get_new_temp("int")
                    head.code += f"{typecast_variable_left} = (int){left.value}\n"
                head.code += f"if {typecast_variable_left} == 0 goto {label2}\n"
                head.code += f"{head.value} = false\n"
                head.code += f"goto {label1}\n"
                head.code += f"{label2}:\n"
                head.code += f"{head.value} = true\n"
                head.code += f"{label1}:\n"
                return

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

            # print(head.operator.value + " ?")
            left = head.left

            head.next = parser.get_new_label()
            left.next = head.next

            AstNode.generateCode(left, parser)

            head.code = left.code + '\n'

        # ------------------------------------------------------------

        elif head.operator == Operator.A_SWITCH:

            left, right = head.left, head.right

            head.value = left
            right.value = head.value
            right.next = head.next
            # print('a_switch', right.next)

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

            head.code = "ifFalse " + head.value.value + " == " + constant[1] + " goto " + statements.next + \
                statements.code + "\n" + statements.next + ":\n"

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
                # if the left operand datatype does not match the combined head datatype, it needs to undergo a widening implicit typecast
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{typecast_variable} = ({head.data_type}) {expr0.value}\n"
                head.code += f"{head.value} = {typecast_variable} + {expr1.value}\n"

            elif head.data_type != expr1.data_type:
                # similarly, if the right operand datatype does not match the combined head datatype, it needs to undergo a widening implicit typecast
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{typecast_variable} = ({head.data_type}) {expr1.value}\n"
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
                    head.code += f"{typecast_variable} = ({head.data_type}){expr1.value}\n"
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
                head.code += f"{typecast_variable} = ({head.data_type}) {expr0.value}\n"
                head.code += f"{head.value} = {typecast_variable} * {expr1.value}\n"

            elif head.data_type != expr1.data_type:
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{typecast_variable} = ({head.data_type}) {expr1.value}\n"
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

            #print('1', expr0.code, '2', expr1.code)
            head.code = expr0.code + "\n" + expr1.code + "\n"

            if head.data_type != expr0.data_type:
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{typecast_variable} = ({head.data_type}) {expr0.value}\n"
                head.code += f"{head.value} = {typecast_variable} / {expr1.value}\n"

            elif head.data_type != expr1.data_type:
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{typecast_variable} = ({head.data_type}) {expr1.value}\n"
                head.code += f"{head.value} = {expr0.value} / {typecast_variable}\n"
            else:
                head.code += f"{head.value} = {expr0.value} / {expr1.value}\n"
        # --------------------------------------------------------------------

        elif head.operator == Operator.A_MODULO:

            expr0, expr1 = head.left, head.right

            head.value = parser.get_new_temp(head.data_type)

            AstNode.generateCode(expr0, parser)
            AstNode.generateCode(expr1, parser)

            # head.code = expr0.code + "\n" + expr1.code + "\n" + \
            # head.value + " = " + expr0.value + " % " + expr1.value

            head.code = expr0.code + "\n" + expr1.code + "\n"

            if head.data_type != expr0.data_type:
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{typecast_variable} = ({head.data_type}) {expr0.value}\n"
                head.code += f"{head.value} = {typecast_variable} % {expr1.value}\n"

            elif head.data_type != expr1.data_type:
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{typecast_variable} = ({head.data_type}) {expr1.value}\n"
                head.code += f"{head.value} = {expr0.value} % {typecast_variable}\n"
            else:
                head.code += f"{head.value} = {expr0.value} % {expr1.value}\n"

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
            num_dimensions = len(variable[0]["dimension"])

            cur = array_variable
            while cur.operator == Operator.A_ARR_EXPR_REC:
                num_dimensions -= 1
                cur = cur.left

            if num_dimensions != 0:
                AstNode.raise_error(
                    f'Semantic Error: Inappropriate usage of the array variable \"{array_variable.value["varname"]}\".')

            # temp = parser.get_new_temp(data_type)
            temp = parser.get_new_temp("int")

            if data_type == INT:
                size = 4
            elif data_type == CHAR:
                size = 1
            elif data_type == FLOAT:
                size = 4
            elif data_type == BOOL:
                size = 1

            # int_temp = parser.get_new_temp("int")

            head.value = array_variable.value["varname"] + "[" + temp + "]"
            head.code = array_variable.code + "\n" + \
                temp + " = " + \
                array_variable.value["val"] + " * " + \
                str(size) + '\n'

        # --------------------------------------------------------------------

        # semantic analysis is required here

        elif head.operator == Operator.A_ARR_EXPR_REC:

            if head.right is not None:
                array_var_use, expr = head.left, head.right

                AstNode.generateCode(array_var_use, parser)
                AstNode.generateCode(expr, parser)

                # temp = parser.get_new_temp(head.data_type)
                temp = parser.get_new_temp("int")
                # head.value["val"] = parser.get_new_temp(head.data_type)
                head.value["val"] = parser.get_new_temp("int")

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

                head.code = array_var_use.code + expr.code + temp + " = " + expr.value + " * " + str(dimension) + "\n" + \
                    head.value["val"] + " = " + \
                    array_var_use.value["val"] + " + " + temp + "\n"

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
                # print("i", index)
                # print(variable[0]["dimension"])
                for j in range(i, len(variable[0]["dimension"])):
                    dimension *= variable[0]["dimension"][j]

                # head.value["val"] = parser.get_new_temp(head.data_type)
                head.value["val"] = parser.get_new_temp("int")
                head.code = expr.code + "\n" + \
                    head.value["val"] + " = " + \
                    expr.value + " * " + str(dimension) + "\n"

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_ASSIGN_STMT:
            left_value, expr = head.left, head.right

            AstNode.generateCode(left_value, parser)
            AstNode.generateCode(expr, parser)

            head.code = left_value.code + "\n" + expr.code + "\n"

            # left_value.value + " = " + expr.value

            # head.value = parser.get_new_temp(head.data_type)

            # AstNode.generateCode(expr0, parser)

            # head.code = expr0.code + "\n" +  \
            #     head.value + " = " + " - " + expr0.value
            # head.code = expr0.code + "\n"

            if head.data_type != expr.data_type and head.data_type == "fuzzy":
                typecast_variable = parser.get_new_temp(expr.data_type)
                head.code += f"{typecast_variable} = ({expr.data_type}) {expr.value}\n"
                head.code += f"{left_value.value} = {typecast_variable}\n"
            elif head.data_type != expr.data_type:
                typecast_variable = parser.get_new_temp(head.data_type)
                head.code += f"{typecast_variable} = ({head.data_type}) {expr.value}\n"
                head.code += f"{left_value.value} = {typecast_variable}\n"
            else:
                head.code += f"{left_value.value} = {expr.value}\n"

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_DECL:

            left = head.left

            # to distinguish between init and declaration
            if head.right is not None:
                # initialization
                right = head.right

                AstNode.generateCode(right, parser)

                head.code = right.code + "\n" + \
                    left[1] + " = (" + left[0] + ") " + right.value + "\n"

            else:
                # declaration
                head.code = left[1] + " = (" + left[0] + ") "
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

            array_list.data_type = head.data_type
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

            dimension_prod = int(math.prod(array_rec.value['list']))
            if dimension_prod != len(array_list.value):
                AstNode.raise_error(
                    "Semantic Error: Array dimension and initialization mismatch")

            head.code = f"{head.data_type} {head.value}[{dimension_prod*size}]\n"

            for i in range(len(array_list.value)):
                head.code += f"{head.value}[{i*size}]={array_list.value[i]}\n"

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_ARR_LITERAL:

            left, right = head.left, head.right

            if right == None:
                if left[0].value.split(' ')[0] != head.data_type:
                    AstNode.raise_error(
                        "Semantic Error: Array initialization datatype mismatch")
                head.value = [left[1]]
                head.code = ""

            else:
                left.data_type = head.data_type
                AstNode.generateCode(left, parser)
                if right[0].value.split(' ')[0] != head.data_type:
                    AstNode.raise_error(
                        "Semantic Error: Array initialization datatype mismatch")
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

            left = head.left
            # print('unique here', left.value)

            AstNode.generateCode(left, parser)
            temp_false = "" if head.false is None else "\ngoto " + head.false
            temp_true = "" if head.true is None else "\ngoto " + head.true

            if left.operator == Operator.A_VARIABLE or left.operator == Operator.A_PLUS or left.operator == Operator.A_MINUS or \
                    left.operator == Operator.A_MULTIPLY or left.operator == Operator.A_DIVIDE or \
                    left.operator == Operator.A_MODULO:

                # print("left.code", left.value is one)
                head.code = left.code + "\n" + "if " + left.value + \
                    " " + "!=" + " 0 goto " + head.true + temp_false

            else:
                if left.operator == Operator.A_INTCONST and left.value == "0":
                    head.code = temp_false
                elif left.operator == Operator.A_STRINGCONST and left.value == "":
                    head.code = temp_false
                elif left.operator == Operator.A_CHARCONST and left.value == "'\\0'":
                    head.code = temp_false
                elif left.operator == Operator.A_FLOATCONST and left.value == "0.0":
                    head.code = temp_false
                else:
                    head.code = 'goto ' + head.true
        # ---------------------------------------------------------------------------------

        elif head.operator == Operator.A_BREAK:
            cur = head
            while(cur.operator != Operator.A_FOR and
                    cur.operator != Operator.A_WHILE and
                    cur.operator != Operator.A_SWITCH
                  ):
                if cur.operator != Operator.A_ROOT:
                    cur = cur.parent
                else:
                    AstNode.raise_error(
                        'Semantic Error : \"break\" can only be used in a for_loop or a while_loop or a switch_case.\n')

            head.code = "goto " + cur.next

        elif head.operator == Operator.A_RETURN:

            left = head.left

            cur = head
            while cur.operator != Operator.A_FUNC:
                cur = cur.parent

            if (left != None and left.data_type != cur.value["return_type"]):
                AstNode.raise_error(
                    f'Semantic Error: return type of the function \"{cur.value["return_type"]}\" ' +
                    f'doesn\'t match with the datatype \"{left.data_type}\" of the returned value.\n')

            elif(left == None and cur.value["return_type"] != "void"):
                AstNode.raise_error(
                    f'Semantic Error: return type of the function \"void\" ' +
                    f'doesn\'t match with the datatype \"{left.data_type}\" of the returned value.\n')

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
                    AstNode.raise_error(
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

        elif head.operator == Operator.A_INPUT:

            left_value = head.left

            if left_value.operator == Operator.A_VARIABLE:
                # print(left_value.value)
                # data_type = parser.get_data_type(left_value.value)
                head.code = f"input {left_value.data_type}, {left_value.value}\n"
            else:
                # data_type = parser.get_data_type(left_value.value.split('[')[0])
                # head = left_value.code
                AstNode.generateCode(left_value, parser)
                cur = left_value
                while cur.left:
                    cur = cur.left

                head.code = left_value.code
                head.code += f"input {cur.data_type}, {left_value.value}\n"

        elif head.operator == Operator.A_OUTPUT:

            left_value = head.left

            # TODO: convert all lists to node
            if type(left_value) == list:
                head.code = f"output {left_value[0].value.split(' ')[0]}, {left_value[1]}\n"
            elif left_value.operator == Operator.A_VARIABLE:
                # print(left_value.value)
                # data_type = parser.get_data_type(left_value.value)
                head.code = f"output {left_value.data_type}, {left_value.value}\n"
            else:
                # data_type = parser.get_data_type(left_value.value.split('[')[0])
                # head = left_value.code
                AstNode.generateCode(left_value, parser)
                cur = left_value
                while cur.left:
                    cur = cur.left

                head.code = left_value.code
                head.code += f"output {cur.data_type}, {left_value.value}\n"
