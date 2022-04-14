from sly import Lexer as SlyLexer


class Lexer(SlyLexer):

    tokens = {PLUS, MINUS, MULT, DIVIDE, MOD, ASSIGN, LPAREN, RPAREN, LSQB, RSQB, COMMA, INTVAL, FLOATVAL, CHARVAL, STRINGVAL, BOOLVAL,
              LBRACE, RBRACE, SEMICOL, COLON, VARNAME, IF, ELSE, WHILE, FOR, ELIF, RETURN, BREAK, CONTINUE, FUNCNAME, DATATYPE, RELOP1, 
              RELOP2, AND, OR, NOT, INPUT, OUTPUT, SWITCH, CASE, DEFAULT, FUZZY, INPUT_STRING}

    ignore = ' \t'
    ignore_comment = r'``(.|\n)[^``]*``'
    ignore_newline = r'\n+'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    @_(r'``(.|\n)[^``]*``')
    def ignore_comment(self, t):
        if len(t.value.split('\n')) > 1:
            self.lineno += (len(t.value.split('\n'))-1)

    # Tokens
    PLUS = r'\+'
    MINUS = r'-'
    MULT = r'\*'
    DIVIDE = r'/'
    MOD = r'%'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'{'
    RBRACE = r'}'
    LSQB = r'\['
    RSQB = r'\]'
    RELOP1 = r'<=|>=|<|>'
    RELOP2 = r'==|!='
    NOT = r'!'
    ASSIGN = r'='
    AND = r'&&'
    OR = r'\|\|'
    COMMA = r','
    SEMICOL = r';'
    COLON = r':'
    FLOATVAL = r'(\d+\.\d+)|(\d+\.)'
    INTVAL = r'\d+'
    CHARVAL = r'\'\w\''
    STRINGVAL = r'\"[^\"]*\"'
    VARNAME = r'[a-zA-Z][a-zA-Z0-9_]*'
    FUNCNAME = r'@[a-zA-Z][a-zA-Z0-9_]*'
    VARNAME['if'] = IF
    VARNAME['else'] = ELSE
    VARNAME['while'] = WHILE
    VARNAME['for'] = FOR
    VARNAME['elif'] = ELIF
    VARNAME['return'] = RETURN
    VARNAME['break'] = BREAK
    VARNAME['continue'] = CONTINUE
    VARNAME['int'] = DATATYPE
    VARNAME['float'] = DATATYPE
    VARNAME['char'] = DATATYPE
    VARNAME['string'] = DATATYPE
    VARNAME['bool'] = DATATYPE
    VARNAME['void'] = DATATYPE
    VARNAME['true'] = BOOLVAL
    VARNAME['false'] = BOOLVAL
    VARNAME['input'] = INPUT
    VARNAME['input_string'] = INPUT_STRING
    VARNAME['output'] = OUTPUT
    VARNAME['switch'] = SWITCH
    VARNAME['case'] = CASE
    VARNAME['default'] = DEFAULT
    VARNAME['fuzzy'] = FUZZY

    def error(self, t):
        print("----Illegal character '%s'----" % t.value[0])
        self.index += 1


if __name__ == '__main__':
    test_case = open('../TestSuites/Palindrome.sq', 'r')
    lexer = Lexer()
    for token in lexer.tokenize(test_case.read()):
        print('type=%r, value=%r' % (token.type, token.value))
    test_case.close()
