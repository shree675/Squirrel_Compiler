from sly import Parser as SlyParser
import sys
import os
sys.path.append(os.path.abspath('../LexicalAnalysis'))
import lexer

class Parser(SlyParser):

    tokens = lexer.Lexer.tokens

    precedence = (
        ('right', 'ASSIGN'),
        ('left', 'LOGOP'),
        ('left', 'RELOP'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIVIDE', 'MOD'),
        ('right', 'NOT'),
        ('right', 'UMINUS')        # fictitious token
    )

    # statement -> expr {return expr}
    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return str('('+p.expr0+'+'+p.expr1+')')

    @_('expr MINUS expr')
    def expr(self, p):
        return str('('+p.expr0+'-'+p.expr1+')')

    @_('expr MULT expr')
    def expr(self, p):
        return str('('+p.expr0+'*'+p.expr1+')')

    @_('expr DIVIDE expr')
    def expr(self, p):
        return str('('+p.expr0+'/'+p.expr1+')')

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return str('(-'+p.expr+')')

    @_('INTVAL')
    def expr(self, p):
        return str(p.INTVAL)


if __name__ == '__main__':
    lex = lexer.Lexer()
    parser = Parser()

    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lex.tokenize(text))
            print(result)
        except EOFError:
            print(EOFError)
            break
