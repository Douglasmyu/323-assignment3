from lexer import *
import sys

# basically runs through the lexer program from A1 but shoves the tokens and lexemes in a list that the parser will call
def getTokens(filename, tokensList):
    isComment = False
    with open(filename, 'r') as f:
        ch = f.read(1)
        while ch:
            buffer = ''
            # handling comments
            if ch == '[':
                nextCh = f.read(1)
                if nextCh == '*':
                    isComment = True
                else:
                    buffer += ch
                    ch = nextCh 
                    continue
            elif isComment and ch == '*':
                nextCh = f.read(1)
                if nextCh == ']':
                    isComment = False
                    ch = f.read(1)
                    continue
            if isComment:
                ch = f.read(1)
                continue
            
            # read in ch until hitting delim
            while ch not in DELIMITERS and ch not in OPERATORS:
                buffer += ch
                ch = f.read(1)
            # if there is something in buffer call lexer for token and print
            if buffer:
                token = lexer(buffer)[0]
                lexeme = lexer(buffer)[1]
                if token:  
                    tokensList.append([token, lexeme])
            # if current char is a separator print separator
            if ch in SEPARATORS:
                token = lexer(ch)[0]
                if token:
                    tokensList.append([token, ch])
            if ch in OPERATORS:
                next = f.read(1)
                if ch + next in MULT_OPS:
                    tokensList.append(['OPERATOR', ch + next])
                    ch = f.read(1) 
                    token = lexer(ch)[0]
                else:
                    f.seek(f.tell() - 1)
                    tokensList.append(['OPERATOR', ch])
            ch = f.read(1)

def advance():
    global token_index
    global tokens_list
    if tokens_list[token_index] is not None:
        token_index += 1

# compares lexeme with expected and progresses token index and prints the token processed
def is_token(expected):
    global token_index
    global tokens_list
    # compares current lexeme with expected 
    if tokens_list[token_index][1] == expected:
        print(f'Matched Token: {tokens_list[token_index]}, Lexeme: {tokens_list[token_index][1]}')
        advance()
        return True
    else:
        return False
               
# error handling needs more work
def syntax_error(expected):
    global token_index
    global token_list
    currentToken = tokens_list[token_index][0]
    currentLexeme = tokens_list[token_index][1]
    error_message = {
        f"SYNTAX ERROR "
        f"Expected: {expected}"
        f"Found Lexeme: {currentLexeme} "
        f"Found Token: {currentToken} "
        f"Current Index: {token_index} "
    }
    raise SyntaxError(error_message)


#production rules
def Rat23F():
    print('<Rat23F> --> <Opt Function Definitions> # <Opt Declaration List> <Statement List> #')
    Opt_Function_Definitions()
    if not is_token('#'):
        syntax_error('#')
    Opt_Declaration_List()
    Statement_List()
    if not is_token('#'):
        syntax_error('#')   
    return True
    
def Opt_Function_Definitions():
    # looking to see if the current position could start <Function>
    if tokens_list[token_index][1] == 'function':
        print('<Opt Function Definitions> --> <Function Definitions>')
        Function_Definitions()
    # if <Function> could not be started then do nothing
    else:
        print('<Opt Function Definitions> --> <Empty>')
        Empty()

def Function_Definitions():
    print('<Function Definitions> --> <Function> <Function Definitions> | <Function Definitions> --> <Function>')
    Function()
    if tokens_list[token_index][1] == 'function':
        # looking to see if the current position could start <Function>
        Function_Definitions()

def Function():
    global token_index
    global tokens_list
    print('<Function> --> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>')
    if not is_token('function'):
        syntax_error('function')
    Identifier()
    if not is_token('('):
        syntax_error('(')
    Opt_Parameter_List()
    if not is_token(')'):
        syntax_error(')')
    Opt_Declaration_List()
    Body()
            
def Opt_Parameter_List():
    # checks the current token to see if <Parameter> can run
    nextToken = tokens_list[token_index + 1][1]
    # checking if current token can run <IDs>
    if isID(tokens_list[token_index][1]):
        print('<Opt Parameter List> --> <Parameter List>')
        # checks if next token can run <Qualifier> therby confirming <Parameter> can run
        if nextToken == 'integer' or nextToken == 'bool' or nextToken == 'real':
            Parameter_List()
    # else do nothing
    else:
        print('<Opt Parameter List> --> <Empty>')
        Empty()

def Parameter_List():
    global tokens_list
    global token_index
    print('<Parameter List> --> <Parameter> , <Parameter List> | <Parameter>')
    # parses Parameter() regardless
    Parameter()
    # checks the next two tokens to see if Parameter could be run
    if tokens_list[token_index][1] == ',':
        if isID(tokens_list[token_index + 1][1]):
            is_token(',')
            Parameter_List()
    
def Parameter():
    print('<Parameter> --> <IDs> <Qualifier>')
    IDs()
    Qualifier()

def Qualifier():
    global token_index
    global tokens_list
    if tokens_list[token_index][1] == 'integer':
        print('<Qualifier> --> integer')
        is_token('integer') 
    elif tokens_list[token_index][1] == 'bool':
        print('<Qualifier> --> bool')
        is_token('bool')
    elif tokens_list[token_index][1] == 'real':
        print('<Qualifier> --> real')
        is_token('real')
    else:
        syntax_error('integer, bool, real')
    
def Body():
    print('<Body> --> { <Statement List> }')
    if not is_token('{'):
        syntax_error('{')
    Statement_List()
    if not is_token('}'):
        syntax_error('}')

def Opt_Declaration_List():
    global tokens_list
    global token_index
    # checks if token is qualifier which means Decaration List can be called
    if tokens_list[token_index][1] == 'integer' or tokens_list[token_index][1] == 'bool' or tokens_list[token_index][1] == 'real':
        print('<Opt Declaration List> --> <Declaration List>')
        Declaration_List()
    else:
        print('<Opt Declaration List> --> <Empty>')
        Empty()
    
def Declaration_List():
    global tokens_list
    global token_index
    print('<Declaration List> --> <Declaration> ; <Declaration List> | <Declaration> ;')
    Declaration()
    if not is_token(';'):
        syntax_error(';')
    # check to see if declaration can be called again
    if tokens_list[token_index][1] == 'integer' or tokens_list[token_index][1] == 'bool' or tokens_list[token_index][1] == 'real':
        Declaration_List()

def Declaration():
    print('<Declaration> --> <Qualifier> <IDs>')
    Qualifier()
    IDs()
    
def IDs():
    global token_index
    global tokens_list
    print('<IDs> --> <Identifier> | <Identifier>, <IDs>')
    Identifier()
    if tokens_list[token_index][1] == ',':
        if isID(tokens_list[token_index + 1][1]):
            is_token(',')
            IDs()   

def Statement_List():
    global tokens_list
    global token_index
    print('<Statement List> --> <Statement> | <Statement> <Statement List>')
    Statement()
    # check if statement list can be called again aka if statement() can be called again
    if tokens_list[token_index][1] == '{':
        Statement_List()
    elif isID(tokens_list[token_index][1]):
        Statement_List()
    elif tokens_list[token_index][1] == 'if':
        Statement_List()
    elif tokens_list[token_index][1] == 'ret':
        Statement_List()
    elif tokens_list[token_index][1] == 'put':
        Statement_List()
    elif tokens_list[token_index][1] == 'get':
        Statement_List()
    elif tokens_list[token_index][1] == 'while':
        Statement_List()
    
def Statement():
    if tokens_list[token_index][1] == '{':
        print('<Statement> --> <Compound>')
        Compound()
    elif tokens_list[token_index][1] == 'ret':
        print('<Statement> --> <Return>')
        Return()
    elif tokens_list[token_index][1] == 'if':
        print('<Statement> --> <If>')
        If()
    elif tokens_list[token_index][1] == 'put':
        print('<Statement> --> <Print>')
        Print()
    elif tokens_list[token_index][1] == 'get':
        print('<Statement> --> <Scan>')
        Scan()
    elif tokens_list[token_index][1] == 'while':
        print('<Statement> --> <While>')
        While()
    elif isID(tokens_list[token_index][1]):
        print('<Statement> --> <Assign>')
        Assign()
    else:
        syntax_error('Statement')
    

def Compound():
    print('<Compound> --> { <Statement List> }')
    if not is_token('{'):
        syntax_error('{')
    Statement_List()
    if not is_token('}'):
        syntax_error('}')

def Assign():
    print('<Assign> --> <Identifier> = <Expression> ;')
    Identifier()
    if not is_token('='):
        syntax_error('=')
    Expression()
    if not is_token(';'):
        syntax_error(';')

def If():
    global token_index
    global tokens_list
    if not is_token('if'):
        syntax_error('if')
    if not is_token('('):
        syntax_error('(')
    Condition()
    if not is_token(')'):
        syntax_error(')')
    Statement()
    # if token is not endif or else, call syntax error
    if tokens_list[token_index][1] == 'endif':
        is_token('if')
    elif tokens_list[token_index][1] == 'else':
        is_token('else')
        Statement()
        if not is_token('endif'):
            syntax_error('endif')
    else:
        syntax_error('endif, else')

def Return():
    global token_index
    global tokens_list

    if not is_token('ret'):
        syntax_error('ret')
    if tokens_list[token_index][1] == ';':
        print('<Return> --> ret ;')
        is_token(';')
    else:
        print('<Return> --< ret <Expression> ;')
        Expression()
        if not is_token(';'):
            syntax_error(';')                 
                                            
def Print():
    print('<Print> --> put ( <Expression> );')
    if not is_token('put'):
        syntax_error('put')
    if not is_token('('):
        syntax_error('(')
    Expression()
    if not is_token(')'):
        syntax_error(')')
    if not is_token(';'):
        syntax_error(';')

def Scan():
    print('<Scan> --> get (<IDs>)')
    if not is_token('get'):
        syntax_error('get')
    if not is_token('('):
        syntax_error('(')
    IDs()
    if not is_token(')'):
        syntax_error(')')
    if not is_token(';'):
        syntax_error(';')
    
def While():
    print('<While> --> while ( <Condition> ) <Statement>')
    if not is_token('while'):
        syntax_error('while')
    if not is_token('('):
        syntax_error('(')
    Condition()
    if not is_token(')'):
        syntax_error(')')
    Statement()

def Condition():
    print('<Condition> --> <Expression> <Relop> <Expression>')
    Expression()
    Relop()
    Expression()

def Relop():
    global tokens_list
    global token_index
    if tokens_list[token_index][1] == '==':
        print('<Relop> --> ==')
        is_token('==')
    elif tokens_list[token_index][1] == '!=':
        print('<Relop> --> !=')
        is_token('!=')
    elif tokens_list[token_index][1] == '>':
        print('<Relop> --> >')
        is_token('>')
    elif tokens_list[token_index][1] == '<':
        print('<Relop> --> <')
        is_token('<')
    elif tokens_list[token_index][1] == '<=':
        print('<Relop> --> <=')
        is_token('<=')
    elif tokens_list[token_index][1] == '=>':
        print('<Relop> --> =>')
        is_token('=>')
    else:
        syntax_error('Relational Operator')
    
def Expression():
    print("<Expression> --> <Term> <Expression'> ")
    Term()
    Expression_Prime()

def Expression_Prime():
    global tokens_list
    global token_index
    if tokens_list[token_index][1] == ('+'):
        is_token('+')
        print("<Expression'> --> + <Term> <Expression'>")
        Term()
        Expression_Prime()
    elif tokens_list[token_index][1] == ('-'):
        is_token('-')
        print("<Expression'> --> - <Term> <Expression'>")
        Term()
        Expression_Prime()    
    else:
        print("<Expression'> --> ε")
        Empty()
    
def Term():
    print("<Term> --> <Factor> <Term'>")
    Factor()
    Term_Prime()

def Term_Prime():
    global tokens_list
    global token_index
    if tokens_list[token_index][1] == ('*'):
        print("<Term'> --> * <Factor> <Term'>")
        is_token('*')
        Factor()
        Term_Prime()
    elif tokens_list[token_index][1] == ('/'):
        print("<Term'> --> / <Factor> <Term'>")
        is_token('/')
        Factor()
        Term_Prime()
    else:
        print("<Term'> --> ε")
        Empty()
    
def Factor():
    global tokens_list
    global token_index
    if tokens_list[token_index] == ('-'):
        print('<Factor> --> - <Primary>')
        is_token('-')
        Primary()
    else:
        print('<Factor> --> <Primary>')
        Primary()
    
def Primary():
    global tokens_list
    global token_index
    if isInt(tokens_list[token_index][1]):
        print('<Primary> --> <Integer>')
        Integer()
    elif isReal(tokens_list[token_index][1]):
        print('<Primary> --> <Real>')
        Real()
    elif tokens_list[token_index][1] == '(':
        print('<Primary> --> (<Expression>)')
        is_token('(')
        Expression()
        if not is_token(')'):
            syntax_error(')')
    elif tokens_list[token_index][1] == 'true':
        print('<Primary> --> true')
        is_token('true')
    elif tokens_list[token_index][1] == 'false':
        print('<Primary> --> false')
        is_token('false')
    elif isID(tokens_list[token_index][1]):
        print('<Primary> --> <Identifier> | <Primary> --> <Identifier> ( <IDs> )')
        Identifier()
        if tokens_list[token_index][1] == '(':
            is_token('(')
            IDs()
            if not is_token(')'):
                syntax_error(')')
def Empty():
    print('<Empty> --> ε')
    return True

def Identifier():
    global token_index
    global tokens_list
    if isID(tokens_list[token_index][1]):
        print(f'Matched Token: {tokens_list[token_index]}, Lexeme: {tokens_list[token_index][1]}')
        token_index += 1
    else:
        syntax_error('ID')

def Real():
    global token_index
    global tokens_list
    if isReal(tokens_list[token_index][1]):
        print(f'Matched Token: {tokens_list[token_index]}, Lexeme: {tokens_list[token_index][1]}')
        token_index += 1
    else:
        syntax_error('Real')
    
    
def Integer():
    global token_index
    global tokens_list
    if isInt(tokens_list[token_index][1]):
        print(f'Matched Token: {tokens_list[token_index]}, Lexeme: {tokens_list[token_index][1]}')
        token_index += 1
    else:
        syntax_error('Integer')

with open('testCases/testCase1.txt', 'a') as f:
    f.write(' ')

tokens_list = []
token_index = 0
getTokens('testCases/testCase1.txt', tokens_list)
file = open('output.txt', 'w')
sys.stdout = file
if Rat23F():
    print('Parsing Complete')
else:
    print('Parsing Failed')
file.close