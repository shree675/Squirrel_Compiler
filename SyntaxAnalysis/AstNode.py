from enum import Enum

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
    A_NEGATE = "-"
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
    A_FUNC = "func"
    A_NODE = "node"
    A_ROOT = "root"
    A_DECL = "decl"
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


class AstNode:
    '''
    If a node contains 2 children, they must be assigned to the left and right attributes
    If a node contains 1 child, it must be assigned to the left child
    '''

    def __init__(self, operator=None, left=None, mid=None, right=None, value=None, next_label=None):
        self.operator = operator
        self.left = left
        self.mid = mid
        self.right = right
        self.value = value

        self.true = None
        self.false = None

        self.code = None
        self.next = next_label

    @staticmethod
    def generateCode(head, get_new_label, get_new_temp):

        if head is None:
            return

        # --------------------------------------------------

        if head.operator == Operator.A_ROOT:

            AstNode.generateCode(head.left, get_new_label, get_new_temp)
            head.code = head.left.code

            with open("output.tac", "w") as f:
                f.write(head.code)

            # print(head.code)

        # --------------------------------------------------

        elif head.operator == Operator.A_NODE:
            left, right = head.left, head.right

            if left and right:
                head.next = get_new_label()
                right.next = head.next
                left.next = get_new_label()
                AstNode.generateCode(left, get_new_label, get_new_temp)
                head.code = left.code + "\n"
                AstNode.generateCode(right, get_new_label, get_new_temp)
                # head.code += left.next + ":\n" + right.code + "\n" + head.next + ":"
                head.code += left.next + ":\n" + right.code
            elif left:
                head.next = get_new_label()
                left.next = get_new_label()
                AstNode.generateCode(left, get_new_label, get_new_temp)
                head.code = left.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_FUNC:
            params, statements = head.left, head.right

            AstNode.generateCode(statements, get_new_label, get_new_temp)

            head.code = statements.code + "\n" + head.next + ":\n" + "return\n"

        # ------------------------------------------------------------

        elif head.operator == Operator.A_AND:

            left, right = head.left, head.right
            true, false = head.true, head.false

            left.true = get_new_label()
            left.false = false
            right.true = true
            right.false = false

            AstNode.generateCode(left, get_new_label, get_new_temp)
            AstNode.generateCode(right, get_new_label, get_new_temp)

            head.code = left.code + "\n" + left.true + ":" + "\n" + right.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_OR:

            left, right = head.left, head.right
            true, false = head.true, head.false

            left.true = true
            left.false = get_new_label()
            right.true = true
            right.false = false

            AstNode.generateCode(left, get_new_label, get_new_temp)
            AstNode.generateCode(right, get_new_label, get_new_temp)

            head.code = left.code + "\n" + left.false + ":" + "\n" + right.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_RELOP1 or head.operator == Operator.A_RELOP2:

            left, right = head.left, head.right
            relop = head.value

            AstNode.generateCode(left, get_new_label, get_new_temp)
            AstNode.generateCode(right, get_new_label, get_new_temp)

            head.code = left.code + "\n" + right.code + "\n" + \
                "if " + left.value + " " + relop + " " + right.value + " goto " + head.true + \
                "\n" + "goto " + head.false

        # ------------------------------------------------------------

        elif head.operator == Operator.A_NOT:

            left = head.left
            true, false = head.true, head.false

            left.true = false
            left.false = true

            AstNode.generateCode(left, get_new_label, get_new_temp)

            head.code = left.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_IF or head.operator == Operator.A_ELIFSINGLE:

            expr, statements = head.left, head.right

            expr.true = get_new_label()
            expr.false = head.next
            statements.next = head.next

            AstNode.generateCode(expr, get_new_label, get_new_temp)
            AstNode.generateCode(statements, get_new_label, get_new_temp)

            head.code = expr.code + "\n" + expr.true + ":\n" + statements.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_IFELSE or head.operator == Operator.A_ELIFMULTIPLE or head.operator == Operator.A_IFELIFELSE:

            expr, statements1, statements2 = head.left, head.mid, head.right

            expr.true = get_new_label()
            expr.false = get_new_label()
            statements1.next = head.next
            statements2.next = head.next

            AstNode.generateCode(expr, get_new_label, get_new_temp)
            AstNode.generateCode(statements1, get_new_label, get_new_temp)
            AstNode.generateCode(statements2, get_new_label, get_new_temp)

            head.code = expr.code + "\n" + expr.true + ":\n" + statements1.code + "\n" + \
                "goto " + head.next + "\n" + expr.false + ":\n" + statements2.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_SWITCHPARENT or head.operator == Operator.A_IFPARENT or head.operator == Operator.A_FORPARENT:

            left = head.left

            head.next = get_new_label()
            left.next = head.next

            AstNode.generateCode(left, get_new_label, get_new_temp)

            head.code = left.code + '\n' + left.next + ":\n"

        # ------------------------------------------------------------

        elif head.operator == Operator.A_SWITCH:

            left, right = head.left, head.right

            head.value = left
            right.value = head.value
            right.next = head.next

            AstNode.generateCode(right, get_new_label, get_new_temp)

            head.code = right.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_CASEMULTIPLE:

            single, multiple = head.left, head.right

            multiple.next = head.next
            multiple.value = head.value
            single.value = head.value
            single.next = head.next

            AstNode.generateCode(single, get_new_label, get_new_temp)
            AstNode.generateCode(multiple, get_new_label, get_new_temp)

            head.code = single.code + "\n" + multiple.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_CASESINGLE:

            constant, statements = head.left, head.right

            statements.next = get_new_label()

            AstNode.generateCode(statements, get_new_label, get_new_temp)

            head.code = "ifFalse " + head.value + " == " + constant[1] + " goto " + statements.next + "\n" + \
                statements.code + "\n" + "goto " + head.next + "\n" + statements.next + ":\n"

        # ------------------------------------------------------------

        elif head.operator == Operator.A_DEFAULT:

            statements = head.left

            statements.next = head.next

            AstNode.generateCode(statements, get_new_label, get_new_temp)

            head.code = statements.code + "\n" + "goto " + head.next

        # ------------------------------------------------------------

        elif head.operator == Operator.A_WHILE:

            expr, statements = head.left, head.right

            begin = get_new_label()
            expr.true = get_new_label()
            expr.false = head.next
            statements.next = begin

            AstNode.generateCode(expr, get_new_label, get_new_temp)
            AstNode.generateCode(statements, get_new_label, get_new_temp)

            head.code = begin + ":\n" + expr.code + "\n" + expr.true + ":\n" + statements.code + "\n" + \
                "goto " + begin

        # ------------------------------------------------------------

        elif head.operator == Operator.A_FOR:

            left, mid, right = head.left, head.mid, head.right

            begin = get_new_label()
            left.true = get_new_label()
            left.false = head.next
            mid.next = begin

            AstNode.generateCode(left, get_new_label, get_new_temp)
            AstNode.generateCode(mid, get_new_label, get_new_temp)
            AstNode.generateCode(right, get_new_label, get_new_temp)

            head.code = begin + ":\n" + left.code + "\n" + left.true + ":\n" + right.code + "\n" + \
                mid.code + "\n" + "goto " + begin

        # ------------------------------------------------------------

        elif head.operator == Operator.A_PLUS:

            expr0, expr1 = head.left, head.right

            head.value = get_new_temp()

            AstNode.generateCode(expr0, get_new_label, get_new_temp)
            AstNode.generateCode(expr1, get_new_label, get_new_temp)

            head.code = expr0.code + "\n" + expr1.code + "\n" + \
                head.value + " = " + expr0.value + " + " + expr1.value

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_MINUS:

            expr0, expr1 = head.left, head.right

            if(expr1 == None):
                head.value = get_new_temp()

                AstNode.generateCode(expr0, get_new_label, get_new_temp)

                head.code = expr0.code + "\n" +  \
                    head.value + " = " + " - " + expr0.value

            else:
                head.value = get_new_temp()

                AstNode.generateCode(expr0, get_new_label, get_new_temp)
                AstNode.generateCode(expr1, get_new_label, get_new_temp)

                head.code = expr0.code + "\n" + expr1.code + "\n" + \
                    head.value + " = " + expr0.value + " - " + expr1.value

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_MULTIPLY:

            expr0, expr1 = head.left, head.right

            head.value = get_new_temp()

            AstNode.generateCode(expr0, get_new_label, get_new_temp)
            AstNode.generateCode(expr1, get_new_label, get_new_temp)

            head.code = expr0.code + "\n" + expr1.code + "\n" + \
                head.value + " = " + expr0.value + " * " + expr1.value

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_DIVIDE:

            expr0, expr1 = head.left, head.right

            head.value = get_new_temp()

            AstNode.generateCode(expr0, get_new_label, get_new_temp)
            AstNode.generateCode(expr1, get_new_label, get_new_temp)

            head.code = expr0.code + "\n" + expr1.code + "\n" + \
                head.value + " = " + expr0.value + " / " + expr1.value

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_MODULO:

            expr0, expr1 = head.left, head.right

            head.value = get_new_temp()

            AstNode.generateCode(expr0, get_new_label, get_new_temp)
            AstNode.generateCode(expr1, get_new_label, get_new_temp)

            head.code = expr0.code + "\n" + expr1.code + "\n" + \
                head.value + " = " + expr0.value + " % " + expr1.value

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_ASSIGN_STMT:

            if type(head.left) == str:
                varname, expr = head.left, head.right

                AstNode.generateCode(expr, get_new_label, get_new_temp)

                head.code = expr.code + "\n" + varname + " = " + expr.value

        # --------------------------------------------------------------------

        elif head.operator == Operator.A_DECL:

            left = head.left

            if head.right is not None:
                right = head.right

                AstNode.generateCode(right, get_new_label, get_new_temp)

                head.code = right.code + "\n" + \
                    left[0] + " " + left[1] + " = " + right.value + "\n"

            else:
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

        elif head.operator == Operator.A_BOOLCONST:

            if head.value == "switch":
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
