#global variables
symbol_table = {}
memory_Address = 7000

#procedures 
#memory addressing
def identifiers_exist(identifier):
    return identifier in symbol_table
 
def insert_identifiers(lexeme, data_type):
    global memory_Address
    if not identifiers_exist(lexeme):
        symbol_table[lexeme] = {"memoryLocation": memory_Address, "type": data_type}
        memory_Address+=1
    else:
        print(f"Error: Identifier '{lexeme}' already declared.")

#print all identifier in the table
def print_all_identifiers():
    print("Identifier\tMemory Location\tType")
    for lexeme, data in symbol_table.items():
        print(f"{lexeme}\t\t{data['memoryLocation']}\t\t{data['type']}")

def get_address(identifier):
    if identifiers_exist(identifier):
        return symbol_table[identifier]['memoryLocation']
    else:
        print(f"Error: Identifer '{identifier}' not declared.")
        return