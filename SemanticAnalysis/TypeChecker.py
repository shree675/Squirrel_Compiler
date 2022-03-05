from SyntaxAnalysis import AstNode

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
    def raise_error(datatype, operator):
        raise Exception(
                f"Error : Operator \"{operator}\" not defined on datatypr \"{data_type}\"")
    @staticmethod
    def check_datatype(left_type=None, right_type=None):
        if (left_type == 'str' and right_type != 'str') or (left_type != 'str' and right_type == 'str'):
            raise_error('str', '=')
        return

    @staticmethod
    def return_datatype(left_type=None, right_type=None, operator=AstNode.Operator.A_INTCONST):
        """This method checks the operator, the datatypes of the operands, 
        raises and error if the operator is not defined on the datatype of the operands,
        does implicit typecasting wherever required, then returns the resulting datatype"""
        #print("Return datatype")
        Operator = AstNode.Operator
        """ if Operator.A_INTCONST == operator:
            print("YAY") """
        #print("ISINSTANR")
        #print(isinstance(operator, type)))
        #print(AstNode.Operator)
        #print(Operator.A_INTCONST, Operator.A_INTCONST, operator)
        #print(AstNode.Operator.A_NEGATE, operator)
        #print(left_type, right_type, operator)

        #print(type(operator), type(Operator.A_INTCONST))       
        if str(operator) == str(Operator.A_INTCONST):
            print("test")
            return 'int'
        elif operator == Operator.A_FLOATCONST:
            return 'float'
        elif operator == Operator.A_STRINGCONST:
            return 'str'
        elif operator == Operator.A_BOOLCONST:
            return 'bool'
        elif operator == Operator.A_CHARCONST:
            return 'char'
        
        #------------------------------Unary Operators----------------------------------
        elif operator == Operator.A_NEGATE:
            if left_type == 'int':
                return 'int'
            elif left_type == 'float':
                return 'float'
            elif left_type == 'str':
                raise_error(left_type, operator)
            elif left_type == 'bool':
                print("Implicitly casting from bool to int")
                # TODO: Modify the symbol table here maybe?
                return 'int'
            elif left_type == 'char':
                print("Implicitly casting from char to int")
                # TODO: Modify the symbol table here maybe?
                return 'int'

        elif operator == Operator.A_NOT:
            if left_type == 'int':
                print("Implicitly casting from int to bool")
                # TODO: Modify the symbol table here maybe?
                return 'bool'
            elif left_type == 'float':
                print("Implicitly casting from float to bool")
                # TODO: Modify the symbol table here maybe?
                return 'bool'
            elif left_type == 'str':
                
                return 'bool'
            elif left_type == 'bool':
                return 'bool'
            elif left_type == 'char':
                return 'bool'
        #------------------------------Binary Operators----------------------------------
        elif operator == Operator.A_PLUS or operator == Operator.A_MINUS or operator == Operator.A_MULTIPLY or operator == Operator.A_DIVIDE:
            if left_type == 'str' or right_type == 'str':
                raise_error('str', operator)
            elif left_type == 'int' and right_type == 'int':
                return 'int'
            elif left_type == 'float' and right_type == 'float':
                return 'float'
            elif left_type == 'float' or right_type == 'float':        
                print("Implicitly casting to float")
                # TODO: Modify the symbol table here maybe?
                return 'float'
            else:
                print("Implicitly casting to int")
                # TODO: Modify the symbol table here maybe?
                return 'int'
        elif operator == Operator.A_MODULO:
            if left_type == 'int' and right_type == 'int':
                return 'int'
            elif left_type == 'float' or right_type == 'float' or left_type == 'str' or right_type == 'str':
                raise_error(left_type, operator)
            else:
                print("Implicitly casting to int")
                # TODO: Modify the symbol table here maybe?
                return 'int'
        elif operator == Operator.A_RELOP1 or operator == Operator.A_RELOP2:
            if left_type == 'int' and right_type == 'int':
                return 'bool'
            elif left_type == 'float' and right_type == 'float':
                return 'bool'
            elif left_type == 'str' or right_type == 'str':
                raise_error(left_type, operator)
            elif left_type == 'float' or right_type == 'float':
                print("Implicitly casting to float")
                # TODO: Modify the symbol table here maybe?
                return 'bool'
            else:
                print("Implicitly casting to int")
                # TODO: Modify the symbol table here maybe?
                return 'bool'
        
        elif operator == Operator.A_AND or operator == Operator.A_OR:
            if left_type == 'bool' and right_type == 'bool':
                return 'bool'
            elif left_type == 'float' or right_type == 'float' or left_type == 'str' or right_type == 'str':
                raise_error(left_type, operator) #change error
            else:
                print("Implicitly casting to bool")
                # TODO: Modify the symbol table here maybe?
                return 'bool'
            



            
        return 'fuzzy'