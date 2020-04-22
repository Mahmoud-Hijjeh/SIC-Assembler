""" The output of Pass 2:
1. The object file (.obj)
2. The listing file (.lst)
3. List of errors if happened (duplicate labels, invalid mnemonic,
inappropriate operand...). """


def send_tables(symbol_table, opt_table, literal_tab, directives, prog_name, prog_leng, start_add):

    #open source file to read it
    intermid_file = open("intermid.mdt", "r")

    #read  all input lines
    sic_assembly = intermid_file.readlines()

    #create a .lst file  
    list_file = open("list.lst","w+")

    #create a .obj file
    object_file = open("objectfile.obj","w+")

    error_flag = 0
    text_record=""
    text_record_length=0
    for ind, line in enumerate(sic_assembly):
        
        lit = False
        header_record = ""

        opcode = line[15:21].strip()
        operand = line[22:41].strip()
        #read first input line
        if opcode == 'START' and ind == 0:
            #write listing file
            list_file.write(line)
            
            #create header record 
            blanks = 6-len(str((prog_name)))
            prog_name+=' '*blanks
            start_add="0"*2+str(hex(start_add)[2:])
            prog_leng = (6-len(str(prog_leng)))*'0'+str(hex(prog_leng)[2:])
            header_record +=('H'+prog_name+start_add+prog_leng)
            
            #write header record to object program
            object_file.write(header_record)
            
            #initilize next text record
            text_record = 'T'+"0"*2+line[ind+1][0:5]
            text_record_object_code = "" 
            continue

        if opcode !='END':
 
            
            
            object_code = ""
            indexed="0"
            
 
            if opcode not in directives:
                #first segment of opject code

                #if opcode is opcode
                if opcode in opt_table:
                    object_code += opt_table[opcode]

                #if opcode is litteral
                elif line[14:15] == "=":
                    lit = True
                    if opcode in literal_tab:
                        object_code = str(literal_tab[opcode][0])
                
                elif operand != "":

                    #second and third segment of opject code
                    if operand in symbol_table:
                        object_code += (str(symbol_table[operand]))
    
                    elif operand == "" and lit == False:
                        object_code +="0000"
                    
                    
                    
                    elif operand in symbol_table or operand[1:] in literal_tab:
                        #if '=' in operand:
                            #constantOperand = operand[1:]
                        if operand in literal_tab :
                            add = literal_tab[operand][2]
                            #object_code += (str(lit_add))
                            
                        elif ',X' in operand:
                            indexed = "1"
                            indexed_operand = operand[:-2]
                            add = symbol_table[indexed_operand]
                        else:
                            indexed_operand = operand
                            add = symbol_table[indexed_operand]
                        #take first halfbyte from the operand
                        z = str(add)[0]
                        z = (indexed+bin(int(z, 16))[2:].zfill(3))
                        z = hex(int(z, 2))[2:]
                        object_code += (z+str(add)[1:])
                    else:
                        print("error,the symbol not exist in symbol table")
                        error_flag += 1
                        break
                            

 

            #if opcode is a directive
            elif opcode == "BYTE":
                if operand[0] == 'X':
                    object_code = operand[2:-1]     
                elif operand[0] == 'C':
                    object_code = operand[2:-1].encode("utf-8").hex()
                blanks = 6-len(object_code)
                object_code = "0"*blanks+object_code

            elif opcode == "WORD":
                object_code = hex(int(operand))[2:]
                blanks = 6-len(object_code)
                object_code = "0"*blanks+object_code
 

            #write the object code on .lst file
            blanks = 45-len(line)
            list_file.write(line[:-1]+" "*blanks+object_code+"\n")
 
            
            #line = line.replace("\n","")
            #ist_file.write(line[:]+" "*(20 - len(operand))+object_code+"\n")
            
            if (text_record_length + len(object_code)) <=60 and (opcode !='RESW' and opcode != 'RESB'  and opcode != 'BASE' and opcode != 'LTORG'):
                text_record_object_code +=object_code
                text_record_length += len(object_code)
            else:
                text_record += (hex(len(text_record_object_code))[2:]+text_record_object_code)
                object_file.write("\n"+text_record)
                text_record = 'T'+ '0'*2+line[0:5]
                text_record_length = 0
                text_record_object_code = ""

        #if the line is END line
        else:
            list_file.write(" "*15+line.strip()+"\n")
            end_record = 'E'+"0"*2+hex(int(start_add))[2:]
            object_file.write("\n"+end_record)
                
    
             
            



    
    