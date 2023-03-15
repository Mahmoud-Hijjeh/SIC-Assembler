'''
SicAssembler V16.00 with GUI in Python

'''
""" The output of Pass 1 is:
1. Symbol Table SYBTAB: displayed on the screen.
2. LOCCTR, PRGLTH, PRGNAME, ...
3. Intermediate file (.mdt): Stored on the secondary storage. 
4.My assembler can stop execution if there are errors in Pass 1
"""

# Phase 1
# Student: Mahmoud Majed Hasan Hijjeh 
# ID: (217090)
# Supervisor: Dr. Yousef Salah
# Introduction to Systems Programming course


import guiForm
from tkinter import messagebox
import tkinter as tk

source_code,intermid_file = guiForm.gui_fun()

if source_code == "":
    messagebox.showerror("ERROR ","Please only Browse to get full path of .asm file!\n" \
                                "\n\nError MSG: {0}")
# Open source file to read it
sic_source_file = open(source_code, "r")

# Open OPTAP file to read it
opcode_table_file = open("OPTAB.txt", "r")

# Read  all input lines
sic_assembly = sic_source_file.readlines()

# Read opcode table 
opcode_table = opcode_table_file.readlines()

# Initialize instruction component
label = ""
opcode = ""
operand = 0
comment = ""

# Data Structure and Flags
symbol_table = {}
opt_table = {}
literal_table = {}
literal_tab = {}
prog_name = ""
prog_leng = 0
start_add = 0
error_flag = 0




# Create a .text file 
intermid_file = open(intermid_file+".mdt","w+")

# Initialize a list of directives
directives = ["START", "END", "BYTE", "WORD", "RESB", "RESW", "BASE", "LTORG"]

# Store opcode table in 2D list
for ind, line in enumerate(opcode_table):
    # Read file from third line 
    if ind>1:
        opt_table[line[0:11].split(' ')[0]] = line[12:15].strip()

# Read first input line
first_line = sic_assembly[0]
if first_line[11:20].strip() == "START":
    prog_name =  first_line[0:10].strip()
    start_add = int(first_line[21:39].strip(),16)
    loc_ctr = start_add

    # To save a fixed format in intermediate file 
    blanks = 6-len(str((loc_ctr)))
    #print(loc_ctr)
    #print(str((loc_ctr)))

    # Write line to intemediate file
    if first_line[34:] != "":
        first_line = first_line[:34]+"\n"
    intermid_file.write('{0:02X}'.format(loc_ctr)+" "*blanks+first_line)
    
else:
    loc_ctr = 0

for ind, line in enumerate(sic_assembly):
    
    if line.strip() == "":
        continue
    # Read opcode
    opcode = line[11:20].strip()
    if opcode == "END":
        break
    elif opcode != "START" :
        # If this is not a comment
        if line[0] != '.':
            if line[38:] != "":
                line = line[:38]+"\n"
                
            # Write line to intemediate file
            # Check if that line is LTORG
            if(opcode == "LTORG" or opcode == "BASE"):
                intermid_file.write(" "*6+line)
            else :
                # To save a fixed format in intermediate file
                blanks = 6-len(str(hex(loc_ctr)[2:]))
                intermid_file.write('{0:02X}'.format(loc_ctr)+" "*blanks+line)
            
            # Read label field
            label = line[0:10].strip()
            # If there is a symbol in label field
            if label != "":
                # Search in SYMTAB for LABEL
                # If found
                if label in symbol_table:
                    # Set error flag
                    error_flag = 1
                    print("ERROR, Duplicate symbol!")
                    # Message box display
                    messagebox.showerror("ERROR ","Duplicate symbol!\n" \
                                "\n\nError MSG: {0}")
                    break
                # Else insert [label, LOCCTR] into SYMTAB
                else:
                    symbol_table[label] = '{0:02X}'.format(loc_ctr)

            # Read opcode field
            # Search OPTAB for OPCODE
            # If found
            if opcode in opt_table:
                # Add 3 {instruction length} to LOCCTR
                loc_ctr += 3
            # If not found
            elif opcode in directives:
                if opcode == "WORD":
                    # Add 3 {instruction length}
                    loc_ctr += 3
                elif opcode == "RESW":
                    operand = line[21:39].strip()
                    loc_ctr += 3 * int(operand)
                elif opcode == "RESB":
                    operand = line[21:39].strip()
                    loc_ctr += int(operand)
                elif opcode == "BYTE":
                    operand = line[21:39].strip()
                    # Find the length of constant in bytes and add it to loc_ctr
                    if operand[0] == 'X':
                        loc_ctr += int((len(operand) - 3)/2)
                    elif operand[0] == 'C':
                        loc_ctr += (len(operand) - 3)
                # Place literals into a pool at some location in object program
                elif opcode == "LTORG":
                    for key in literal_table:
                        literal_table[key][2] = '{0:02X}'.format(loc_ctr)
                        blanks = 6-len(str(hex(loc_ctr)[2:]))
                        intermid_file.write('{0:02X}'.format(loc_ctr)+" "*blanks+"*"+" "*7+"="+key+"\n")
                        loc_ctr += int(literal_table[key][1])
                    literal_table = {}
            else:
                # Set error flag
                error_flag = 1
                print("ERROR, Invalid operation code")
                # Message box display
                messagebox.showerror("invalid operation code","Please enter valid operation code\n" \
                                "\n\nError MSG: {0}")
                break
                    
            # Check if line contain literal
            if line[21:22] == '=':
                literalList = []
                isExist = 1
                literal = line[22:39].strip()
                if literal[0]=='C':
                    hexCode = literal[2:-1].encode("utf-8").hex()
                elif literal[0]== 'X':
                    hexCode = literal[2:-1]
                else:
                    # Set error flag
                    error_flag = 1
                    print("invalid literals")
                    # Message box display
                    messagebox.showerror("invalid literals","Please enter valid literal\n" \
                                "E.g.: =C'' or =X''"
                                "\n\nError MSG: {0}")
                # Find literal in table literal

                if literal in literal_tab:
                    isExist = 0
                
                # If literal not exist in literal tabel 
                if isExist:
                    literalList=[hexCode,len(hexCode)/2, 0]
                    literal_table[literal]= literalList
                    literal_tab[literal]= literalList
if line[38:] != "":
    line = line[:38]+"\n"
if(opcode == "END"):
    intermid_file.write(" "*6+line+"\n")

# Place literals into apool at the end of prog
# If not LTORG has came after them 
if literal_table:
    for key in literal_table:
        literal_table[key][2] = '{0:02X}'.format(loc_ctr)
        blanks = 6-len(str(hex(loc_ctr)[2:]))
        intermid_file.write('{0:02X}'.format(loc_ctr)+" "*blanks+"*"+" "*7+"="+key+"\n")
        loc_ctr += int(literal_table[key][1])

# Save (loc_ctr - starting add ) as program length
prog_leng = int(loc_ctr) - int(start_add)

# Close files
sic_source_file.close()
opcode_table_file.close()
intermid_file.close()


if error_flag != 1:
    import pass2 
    pass2.send_tables(symbol_table, opt_table, literal_tab, directives,prog_name, prog_leng, start_add, loc_ctr)
