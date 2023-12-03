from lexer import *

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
            while ch not in DELIMITERS:
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
                    
            ch = f.read(1)

# compares lexeme with expected and progresses token index
def is_token(expected):
    global token_index
    global tokens_list
    # compares current lexeme with expected 
    if tokens_list[token_index][1] == expected:
        token_index += 1
        return True
    return False
               
# error handling needs more work
def syntax_error():
    global token_index
    global token_list
    currentToken = tokens_list[token_index][0]
    currentLexeme = tokens_list[token_index][1]
    print(f'Current Token: {currentToken}')
    print(f'Current Lexeme: {currentLexeme}')
    return False


#production rules
def Rat23F():
    print('<Rat23F> --> <Opt Function Definitions> # <Opt Declaration List> <Statement List> #')
    if Opt_Function_Definitions():
        if is_token('#'):
            if Opt_Declaration_List():
                if Statement_List():
                    if is_token('#'):
                        print(lexer('#'))
                        print(lexer('#'))
                        return True
    return False

def Opt_Function_Definitions():
    if Function_Definitions():
        print('<Opt Function Definitions> --> <Function Definitions>')
        return True
    elif Empty():
        print('<Opt Function Definitions> --> <Empty>')
        return True
    else:
        return False

def Function_Definitions():
    if Function():
        if Function_Definitions():
            print('<Function Definitions> --> <Function> <Function Definitions>')
            return True
        else:
            print('<Function Definitions> --> <Function>')
            return True
    else:
        return False
    

def Function():
    if is_token('function'):
        if Identifier():
            if is_token('('):
                if Opt_Parameter_List():
                    if is_token(')'):
                        if Opt_Declaration_List():
                            if Body():
                                print('<Function> --> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>')
                                print(lexer('('))
                                print(lexer(')'))
                                return True
    else:
        return False
            
def Opt_Parameter_List():
    if Parameter_List():
        print('<Opt Parameter List> --> <Parameter List>')
        return True
    elif Empty():
        print('<Opt Parameter List> --> <Empty>')
        return True
    else:
        return False

def Parameter_List():
    if Parameter():
        if is_token(','):
            print('<Parameter List> --> <Parameter> , <Parameter List>')
            print(lexer(','))
            if Parameter_List():
                return True
        else:
            print('<Parameter List> --> <Parameter>')
            return True
    else:
        return False
    
def Parameter():
    if IDs():
        if Qualifier():
            print('<Parameter> --> <IDs > <Qualifier>')
            return True
    else:
        return False    

   
def Qualifier():
    if is_token('integer'):
        print('<Qualifier> --> integer')
        print(lexer('integer'))
        return True
    elif is_token('bool'):
        print('<Qualifier> --> bool')
        print(lexer('bool'))
        return True
    elif is_token('real'):
        print('<Qualifier> --> real')
        print(lexer('real'))
        return True
    else:
        return False
    
def Body():
    if is_token('{'):
        if Statement_List():
            if is_token('}'):
                print('<Body> --> { <Statement List> }')
                print(lexer('{'))
                print(lexer('}'))
                return True
    return False

def Opt_Declaration_List():
    if Declaration_List():
        print('<Opt Declaration List> --> <Declaration List>')
        return True
    elif Empty():
        print('<Opt Declaration List> --> <Empty>')
        return True
    else: 
        return False
    
def Declaration_List():
    if Declaration():
        if is_token(';'):
            if Declaration_List():
                print('<Declaration List> --> <Declaration> ; <Declaration List>')
                print(lexer(';'))
                return True
            else:
                print('<Declaration List> --> <Declaration> ;')
                print(lexer(';'))
                return True
    else:
        return False
    
def Declaration():
    if Qualifier():
        if IDs():
            print('<Declaration> --> <Qualifier > <IDs>')
            return True
    else:
        return False
    
def IDs():
    if Identifier():
        if is_token(','):
            if IDs():
                print('<IDs> --> <Identifier>, <IDs>')
                print(lexer(','))
                return True
        else:
            print('<IDs> --> <Identifier>')
            return True
    else:
        return False
        

def Statement_List():
    if Statement():
        if Statement_List():
             print('<Statement List> --> <Statement> <Statement List>')
             return True
        else:
            print('<Statement List> --> <Statement>')
            return True
    else:
        return False
    
def Statement():
    if Compound():
        print('<Statement> --> <Compound>')
        return True
    elif Assign():
        print('<Statement> --> <Assign>')
        return True
    elif If():
        print('<Statement> --> <If>')
        return True
    elif Return():
        print('<Statement> --> <Return>')
        return True
    elif Print():
        print('<Statement> --> <Print>')
        return True
    elif Scan():
        print('<Statement> --> <Scan>')
        return True
    elif While():
        print('<Statement> --> <While>')
        return True
    else:
        return False

def Compound():
    if is_token('{'):
        if Statement_List():
            if is_token('}'):
                print('<Compound> --> { <Statement List> }')
                print(lexer('{'))
                print(lexer('}'))
                return True
    else:
        return False

def Assign():
    if Identifier():
        if is_token('='):
            if Expression():
                if is_token(';'):
                    print('<Assign> --> <Identifier> = <Expression> ;')
                    print(lexer('='))
                    print(lexer(';'))
                    return True
    else:
        return False

def If():
    if is_token('if'):
        if is_token('('):
            if Condition():
                if is_token(')'):
                    if Statement():
                        if is_token('endif'):
                            print('<If> --> if ( <Condition> ) <Statement> endif')
                            print(lexer('if'))
                            print(lexer('('))
                            print(lexer(')'))
                            print(lexer('endif'))
                            return True
                        elif is_token('else'):
                            if Statement():
                                if is_token('endif'):
                                    print('<If> --> if ( <Condition> ) <Statement> else <Statement> endif')
                                    print(lexer('if'))
                                    print(lexer('('))
                                    print(lexer(')'))
                                    print(lexer('else'))
                                    print(lexer('endif'))

def Return():
    if is_token('ret'):
        if is_token(';'):
           print('<Return> --> ret ;')
           print(lexer('ret'))
           print(lexer(';'))
           return True
        else:
            if Expression():
                if is_token(';'):
                    print('<Return> --> ret <expression>')
                    print(lexer('ret'))
                    print(lexer(';'))
                    return True
    else:
        return False
                           
                                            
def Print():
    if is_token('put'):
        if is_token('('):
            if Expression():
                if is_token(')'):
                    if is_token(';'):
                        print('<Print> --> put ( <Expression> );')
                        print(lexer('put'))
                        print(lexer('('))
                        print(lexer(')'))
                        print(lexer(';'))
                        return True
    else:
        return False

def Scan():
    if is_token('get'):
        if is_token('('):
            if IDs():
                if is_token(')'):
                    print('<Scan> --> get (<IDs>)')
                    print(lexer('get'))
                    print(lexer('('))
                    print(lexer(')'))
                    return True
    return False
    
def While():
    if is_token('while'):
        if is_token('('):
            if Condition():
                if is_token(')'):
                    if Statement():
                        print('<While> --> while ( <Condition> ) <Statement>')
                        print(lexer('while'))
                        print(lexer('('))
                        print(lexer(')'))
                        return True
    return False

def Condition():
    if Expression():
        if Relop():
            if Expression():
                print('<Condition> --> <Expression> <Relop> <Expression>')
                return True
    return False

def Relop():
    if is_token('=='):
        print('<Relop> --> ==')
        print(lexer('=='))
        return True
    elif is_token('!='):
        print('<Relop> --> !=')
        print(lexer('!='))
        return True
    elif is_token('>'):
        print('<Relop> --> >')
        print(lexer('>'))
        return True
    elif is_token('<'):
        print('<Relop> --> <')
        print(lexer('<'))
        return True
    elif is_token('<='):
        print('<Relop> --> <=')
        print(lexer('<='))
        return True
    elif is_token('=>'):
        print('<Relop> --> =>')
        print(lexer('=>'))
        return True
    else:
        return False
    
def Expression():
    if Term():
        if Expression_Prime():
            print('<Expression> --> <Term> <Expression>')
            return True
    return False

def Expression_Prime():
    if is_token('+'):
        if Term():
            if Expression_Prime():
                print("<Expression'> --> + <Term> <Expression'>")
                print(lexer('+'))
                return True
                
    elif is_token('-'):
        if Term():
            if Expression_Prime():
                print("<Expression'> --> - <Term> <Expression'>")
                print(lexer('-'))
                return True
    elif Empty():
        return True
    else:
        return False
    
def Term():
    if Factor():
        if Term_Prime():
            print("<Term> --> <Factor> <Term'>")
            print('<Factor> <Term')
            return True
    return False

def Term_Prime():
    if is_token('*'):
        if Factor():
            if Term_Prime():
                print("<Term'> --> * <Factor> <Term'>")
                print(lexer('*'))
    elif is_token('/'):
        if Factor():
            if Term_Prime():
                print("<Term'> --> / <Factor> <Term'>")
                print(lexer('/'))
    elif Empty():
        return True
    else:
        return False
    
def Factor():
    if is_token('-'):
        if Primary():
            print('<Factor> --> - <Primary>')
            print(lexer('-'))
            return True
    elif Primary():
        print('<Factor> --> <Primary>')
    else:
        return False
    
def Primary():
    if Identifier():
        print('<Primary> --> <Identifier>')
        return True
    elif Integer():
        print('<Primary> --> <Integer>')
        return True
    elif Identifier():
        if is_token('('):
            if IDs():
                if is_token(')'):
                    print('<Primary> --> <Identifier> (<IDs>)')
                    print(lexer('('))
                    print(lexer(')'))
                    return True
    elif is_token('('):
        if Expression():
            if is_token(')'):
                print('<Primary> --> (<Expression>)')
                print(lexer('('))
                print(lexer(')'))
                return True
    elif Real():
        print('<Primary> --> <Real>')
        return True
    elif is_token('true'):
        print('<Primary> --> true')
        print(lexer('true'))
        return True
    elif is_token('false'):
        print('<Primary> --> true')
        print(lexer('false'))
        return True
    else:
        return False

def Empty():
    print('<Empty> --> epsilon')
    return True

def Identifier():
    global token_index
    global tokens_list
    if isID(tokens_list[token_index][1]):
        print(lexer(tokens_list[token_index][1]))
        token_index += 1
        return True
    else:
        return False

def Real():
    global token_index
    global tokens_list
    if isReal(tokens_list[token_index][1]):
        print(lexer(tokens_list[token_index][1]))
        token_index += 1
        return True
    else:
        return False
    
    
def Integer():
    global token_index
    global tokens_list
    if isInt(tokens_list[token_index][1]):
        print(lexer(tokens_list[token_index][1]))
        token_index += 1
        return True
    else:
        return False
# the main program
tokens_list = []
token_index = 9
getTokens('testCases/testCase1.txt', tokens_list)
# print(tokens_list)
if Rat23F():
    print('Parsing Complete')
else:
    syntax_error()