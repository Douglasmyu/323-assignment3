#global variables
symbolTable = {}
memory_Address = 7000

#memory addressing
def identifiers_exist(lexeme):
    return lexeme in symbolTable


#procedures 
def procedures(identifier):
    print()
    #check if identifier exist
        #if not return error

    #insert the identifier into the table
    #print all identifier in the table
    #if identifier is used without declaring it
        #return error
