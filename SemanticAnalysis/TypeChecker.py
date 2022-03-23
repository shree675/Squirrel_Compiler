from AstNode import AstNode
import logging as logger
logger.exception = logger.error


class TypeChecker:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        #print("Typechecker initialized")
        #print('passed symbol table:', symbol_table)
        #Operator = AstNode.Operator

    """ @staticmethod
    def check(head, symbol_table):
        print("Check method")
        print(head.left, head.operator, head.right) """

    """ @staticmethod
    def return_datatype(self, left_type=None, right_type=None, operator=None, isUnary=False):
        print("Return datatype")
        print(self.symbol_table) """

    @staticmethod
    def raise_error(data_type1=None, operator=None, data_type2=None, condition_type=None):
        try:
            if condition_type != None:
                raise Exception("TypeError: Expected type '{}' but got type '{}' in '{}'".format(
                    condition_type, data_type1, operator.value))

            elif(data_type2 == None):
                raise Exception(
                    f"Semantic Error : Operator \"{operator.value}\" not defined on datatype \"{data_type1}\"")
            else:
                raise Exception(
                    f"Semantic Error : Operator \"{operator.value}\" not defined on datatype \"{data_type1}\" and \"{data_type2}\"")
        except Exception as ex:
            logger.exception(ex)
            quit()
            #logger.exception(f"Looks like they have a problem: {ex}", exc_info=False)
        """ raise Exception(
                f"Error : Operator \"{operator.value}\" not defined on datatype \"{data_type}\"") """

    @staticmethod
    def return_datatype(left_type=None, right_type=None, operator=AstNode.Operator.A_INTCONST):
        """This method checks the operator, the datatypes of the operands, 
        raises and error if the operator is not defined on the datatype of the operands,
        does implicit typecasting wherever required, then returns the resulting datatype"""
        #print("Return datatype")
        Operator = AstNode.Operator
        # print("ISINSTANR")
        # print(isinstance(operator, type)))
        # print(AstNode.Operator)
        #print(Operator.A_INTCONST, Operator.A_INTCONST, operator)
        #print(AstNode.Operator.A_NEGATE, operator)
        #print(left_type, right_type, operator)

        #print(operator, type(Operator.A_INTCONST))
        if operator.value == Operator.A_INTCONST.value:
            #print("int const")
            return 'int'
        elif operator.value is Operator.A_FLOATCONST.value:
            #print("float const")
            return 'float'
        elif operator.value == Operator.A_STRINGCONST.value:
            #print("string const")
            return 'string'
        elif operator.value == Operator.A_BOOLCONST.value:
            #print("bool const")
            return 'bool'
        elif operator.value == Operator.A_CHARCONST.value:
            #print("char const")
            return 'char'

        # ------------------------------Unary Operators----------------------------------
        elif operator.value == Operator.A_NEGATE.value:
            if left_type == 'int':
                return 'int'
            elif left_type == 'float':
                return 'float'
            elif left_type == 'string':
                #print("This is the operator", operator)
                TypeChecker.raise_error(left_type, operator)
            elif left_type == 'bool':
                #print("Implicitly casting from bool to int")
                return 'int'
            elif left_type == 'char':
                #print("Implicitly casting from char to int")
                return 'int'

        elif operator.value == Operator.A_NOT.value:
            if left_type == 'int' or left_type == 'char' or left_type == 'float':
                #print("Implicitly casting from to bool")
                return 'bool'

            elif left_type == 'string':
                TypeChecker.raise_error(left_type, operator)

            elif left_type == 'bool':
                return 'bool'

        # ------------------------------Binary Operators----------------------------------
        elif operator.value == Operator.A_PLUS.value or operator.value == Operator.A_MINUS.value or operator.value == Operator.A_MULTIPLY.value or operator.value == Operator.A_DIVIDE.value:
            if left_type == 'string' or right_type == 'string':
                TypeChecker.raise_error('string', operator)
            elif left_type == 'int' and right_type == 'int':
                return 'int'
            elif left_type == 'float' and right_type == 'float':
                return 'float'
            elif left_type == 'float' or right_type == 'float':
                #print("Implicitly casting to float")
                # : Modify the symbol table here maybe?
                return 'float'
            else:
                #print("Implicitly casting to int")
                # : Modify the symbol table here maybe?
                return 'int'
        elif operator.value == Operator.A_MODULO.value:
            if left_type == 'int' and right_type == 'int':
                return 'int'
            elif left_type == 'float' or right_type == 'float' or left_type == 'string' or right_type == 'string':
                TypeChecker.raise_error(left_type, operator)
            else:
                #print("Implicitly casting to int")
                # : Modify the symbol table here maybe?
                return 'int'
        elif operator.value == Operator.A_RELOP1.value or operator.value == Operator.A_RELOP2.value:
            if left_type == 'int' and right_type == 'int':
                return 'bool'
            elif left_type == 'float' and right_type == 'float':
                return 'bool'
            elif left_type == 'string' or right_type == 'string':
                TypeChecker.raise_error(left_type, operator)
            elif left_type == 'float' or right_type == 'float':
                #print("Implicitly casting to float")
                # : Modify the symbol table here maybe?
                return 'bool'
            else:
                #print("Implicitly casting to int")
                # : Modify the symbol table here maybe?
                return 'bool'

        elif operator.value == Operator.A_AND.value or operator.value == Operator.A_OR.value:
            if left_type == 'bool' and right_type == 'bool':
                return 'bool'
            elif left_type == 'string' or right_type == 'string':
                TypeChecker.raise_error(
                    data_type1=left_type, operator=operator, data_type2=right_type)
            else:
                #print("Implicitly casting to bool")
                # : Modify the symbol table here maybe?
                return 'bool'
        elif operator.value == Operator.A_TYPECAST.value:
            #print("Typecast check")
            if left_type == 'string' or right_type == 'string':
                TypeChecker.raise_error(
                    data_type1='string', condition_type='bool or char or int or float', operator=operator)

        return 'fuzzy'

    @staticmethod
    def check_datatype(expr_type=None, operator=AstNode.Operator.A_WHILE):
        """This method checks the statement type, the datatypes of the expr, 
        raises and error if the statement type is not defined on the datatype of the operands,
        does implicit typecasting wherever required, then returns the resulting datatype"""
        #print("Return datatype")
        Operator = AstNode.Operator
        condition_operators = [Operator.A_WHILE.value, Operator.A_IF.value, Operator.A_IFELSE.value,
                               Operator.A_ELIFSINGLE.value, Operator.A_ELIFMULTIPLE.value, Operator.A_IFELIFELSE.value]

        if operator.value in condition_operators:
            #print("bool condition check")
            if expr_type == 'bool':
                return
            if expr_type == 'string':
                TypeChecker.raise_error(
                    data_type1='string', condition_type='bool or char or int', operator=operator)
        elif operator.value == Operator.A_ARR_EXPR_REC.value:
            #print("Array[expr] int type check")
            if expr_type == 'int':
                return
            else:
                TypeChecker.raise_error(
                    data_type1=expr_type, condition_type='int', operator=operator)

        return
