# -*- Coding: utf-8 -*-
'''
SicAssembler V16.00 with GUI in Python

''' 

""" 
The output of Pass 2:
1. The object file (.obj)
2. The listing file (.lst)
3. List of errors if happened (duplicate labels, invalid mnemonic,
inappropriate operand...). 

"""
# Phase 2
# Student: Mahmoud Majed Hasan Hijjeh 
# ID: (217090)
# Supervisor: Dr. Yousef Salah
# Introduction to Systems Programming course


from tkinter import messagebox
import tkinter as tk


def modify_add(address, indexed, object_code):

    z = str(address)[0]
    z = (indexed+bin(int(z, 16))[2:].zfill(3))
    z = hex(int(z, 2))[2:]
    object_code += (z+str(address)[1:])
    return object_code



def write_to_text_record(object_file, text_record_length, text_record_object_code, text_record):
    text_record += ('{0:02X}'.format(int(text_record_length/2))+"^"+text_record_object_code)
    object_file.write("\n"+text_record)


        


def send_tables(symbol_table, opt_table, literal_tab, directives, prog_name, prog_leng, start_add, loc_ctr):
    text_record_object_code = ""
    # Open source file to read it
    intermid_file = open("intermid.mdt", "r")

    # Read  all input lines
    sic_assembly = intermid_file.readlines()

    # Create .lst file  
    list_file = open("list.lst","w+")

    # Create .obj file
    object_file = open("objectfile.obj","w+")

    error_flag = 0
    text_record=""
    text_record_length=0
    end_exist = False
    
    
    for ind, line in enumerate(sic_assembly):
        lit = False
        header_record = ""

        opcode = line[17:26].strip()
        operand = line[27:48].strip()
        # Read first input line
        if opcode == 'START' and ind == 0:
            # Write listing file
            list_file.write(line)
            
            # Create header record 
            blanks = 6-len(str((prog_name)))
            prog_name+=' '*blanks
            start_add="0"*2+'{0:02X}'.format(int(start_add))
            prog_leng = (6-len(str(prog_leng)))*'0'+'{0:02X}'.format(int(prog_leng))
            header_record +=('H^'+prog_name+'^'+start_add+'^'+prog_leng)
            
            # Write header record to object program
            object_file.write(header_record)
            
            # Initilize next text record
            if ind+1 in range(len(sic_assembly)):
                text_record = 'T^'+"0"*2+sic_assembly[ind+1][0:4].strip()+"^"
                text_record_object_code = "" 
            continue
        
        if opcode != 'START' and ind == 0:
            header_record +=('H^'+prog_name+'^'+"000000"+'^'+hex(prog_leng)[2:])
            start_add = "000000"
            prog_leng = hex(loc_ctr)[2:]
            # Write header record to object program
            object_file.write(header_record)
            
            # Initilize next text record
            text_record = 'T^'+"0"*2+sic_assembly[ind+1][0:4].strip()+"^"
            text_record_object_code = ""
        # If opcode !='END':

        object_code = ""      
        if opcode not in directives:
            # First segment of object code

            # If opcode in opcode table
            if opcode in opt_table:
                object_code += opt_table[opcode]

            # If opcode is litteral
            elif line[16:17] == "=":
                lit = True
                if opcode in literal_tab:
                    object_code = str(literal_tab[opcode][0])

            
            # Second and third segment of object code
            if operand in symbol_table:
                add = symbol_table[operand]
                object_code = modify_add(add, "0", object_code)


            elif operand == "" and lit == False:
                object_code +="0000"

            elif ',X' in operand:
                # Take first half byte from the operand
                operand = operand[:-2]
                add = symbol_table[operand]
                object_code = modify_add(add, "1", object_code)

            elif '=' in operand:
                operand = operand[1:]
                if operand in literal_tab :
                    add = literal_tab[operand][2]
                    object_code = modify_add(add, "0", object_code)

            elif lit == False:
                print(ind)
                print("ERROR!, you are using a not correct symbol")
                error_flag += 1
                messagebox.showerror("invalid operand ","Please use a correct symbol\n" \
                                "\n\nError MSG: {0}")
                break

        # If opcode is a directive
        elif opcode == "BYTE":
            if operand[0] == 'X':
                object_code = operand[2:-1]     
            elif operand[0] == 'C':
                object_code = operand[2:-1].encode("utf-8").hex()
            object_code =object_code

        elif opcode == "WORD":
            object_code = hex(int(operand))[2:]
            blanks = 6-len(object_code)
            object_code = "0"*blanks+object_code

        # Write the object code on .lst file
        blanks = 45-len(line)
        list_file.write(line[:-1]+" "*blanks+object_code+"\n")

        discnt = False
        if opcode == "RESW" or opcode == "RESB":
            discnt = True
        
        if discnt and ind+1 not in range(len(sic_assembly)):
            write_to_text_record(object_file, text_record_length, text_record_object_code, text_record)
            break
            

        
        if (discnt == True) and (sic_assembly[ind+1][17:26].strip()!='RESW' and sic_assembly[ind+1][17:26].strip()!='RESB'): 
            write_to_text_record(object_file, text_record_length, text_record_object_code, text_record)
            text_record = 'T^'+'0'*2+sic_assembly[ind+1][0:4]+"^"
            text_record_length = 0
            text_record_object_code = ""           
        

        elif text_record_length + len(object_code) <=60 and discnt == False:
            text_record_object_code +=object_code+"^"
            text_record_length += len(object_code)
            
        elif discnt == False:
            write_to_text_record(object_file, text_record_length, text_record_object_code, text_record)
            text_record = 'T^'+'0'*2+line[0:4]+"^"
            text_record_length = len(object_code)
            text_record_object_code = object_code + "^"
        
        if ind+1 not in range(len(sic_assembly)):
            write_to_text_record(object_file, text_record_length, text_record_object_code, text_record)
            

        # If the line is END line
        if opcode == "END":
            end_exist = True
        

    if end_exist == True:
        end_record = 'E^'+start_add
        object_file.write("\n"+end_record)
    
      
    loc_ctr=hex(loc_ctr)[2:]
    
    # Close files
    object_file.close()
    list_file.close()
    intermid_file.close()

    if error_flag != 1:
        pl = str(prog_leng) 
        lc = str(loc_ctr) 
        '''
        print("name of the program: ",prog_name)
        print("length of the program: ",pl)
        print("LOCCTR: ",lc)
        print("symbol table : ",symbol_table)
        print("literal table : ",literal_tab)
    '''
        SymbolTable = "\nSymbol"+" "*4+"address\n"
        for Symbol in symbol_table:
            blanks = 8-len(Symbol)
            SymbolTable += (Symbol+" "*blanks+"  "+ symbol_table[Symbol] + '\n')
    
        literalTable = "\nliteral"+" "*3+"value"+" "*9+"length"+" "*3+"address\n"
        for literal in literal_tab:
            blanks = 10-len(str(literal))
            b = blanks*2
            literalTable += (literal+" "*blanks+ str(literal_tab[literal][0])+" "*b+str(literal_tab[literal][1])+" "*9+str(literal_tab[literal][2]) + '\n')
    
        root = tk.Tk()
        root.title("Assembler Output ")
        programName = tk.Text(root, height=60, width=80)
        programName.pack()
        quote = "\n\nprogram name: "+prog_name+"\n\nLocation counter: "+lc+"\n\nthe length of the program: "+pl+"\n\nSYMTAB: "+SymbolTable+"\n\nLITTAB: "+literalTable+"\n\n the intermediate file has been successfully extracted into 'intermid.mdt'\n\n the listing file has been successfully extracted into 'list.lst' \n\n the program file has been successfully extracted into 'objectfile.obj' "
        programName.insert(tk.END, quote)
        # B = tk.Button(root, text ="open intermidiate file", command = lambda:openIntermidiateFile)

        # B.pack()
    
        root.mainloop()
