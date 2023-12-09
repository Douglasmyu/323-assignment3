#global variables
symbolTable = [[lexeme],[memory_Address]]
memory_Address = 7000

#procedures 
#memory addressing
def identifiers_exist(identifier):
    if identifier in symbolTable:
        return identifier in symbolTable
 
 
#check if identifier exist
    #if not return error
def insert_identifiers(lexeme, data_type):
    global memory_Address
    if not identifiers_exist(lexeme):
        symbolTable[lexeme] = {"memoryLocation": memory_Address, "type": data_type}
        memory_Address+=1
    else:
        print(f"Error: Identifier '{lexeme}' already declared.")

#print all identifier in the table
def print_all_identifiers():
    print("Identifier\tMemory Location\tType")
    for lexeme, data in symbolTable.items():
        print(f"{lexeme}\t\t{data['MemoryLocation']}\t\t{data['Type']}")
