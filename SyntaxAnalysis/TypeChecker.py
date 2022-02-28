
class TypeChecker:
    def __init__(self):
        print("Typechecker initialized")
        

    @staticmethod
    def check(head, symbol_table):
        print("Check method")
        print(head.left, head.operator, head.right)