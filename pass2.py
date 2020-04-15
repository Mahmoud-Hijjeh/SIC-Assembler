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

    #create a .lst files  
    list_file = open("list.lst","w+")

    #create a .obj files  
    object_file = open("objectfile.obj","w+")

    error_flag = 0
    text_record=""
    text_record_length=0
    for ind, line in enumerate(sic_assembly):

        header_record = ""

        opcode = line[15:21].strip()
        operand = line[22:41].strip()

        #read first input line
        if opcode == 'START' and ind == 0:
            #write listing file
            list_file.write(line)
            
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
            
            indexed='0'
            object_code = ""
            
            if opcode not in directives:
    
                #first segment of opject code
                if opcode in opt_table:
                    object_code += opt_table[opcode]
    
                #second segment of opject code
                if ",X" in operand:
                    indexed= "1"
    
                #third segment of opject code
                if operand in symbol_table:
                    z = str(symbol_table[operand])[0]
                    z = (indexed+bin(int(z, 16))[2:].zfill(3))
                    z = int(z, 2)
                    z = hex(z)[2:]
                    object_code += (z+str(symbol_table[operand])[1:])
                if operand == "":
                    object_code +="0000"
                

    
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
            
            
            elif opcode[0]=="=":
                
                if opcode in literal_tab:
                    object_code = literal_tab[opcode[3:-1]][0]
            
             
            list_file.write(line[:-1]+"  "+object_code)
            
            if text_record_length + len(object_code) <=60:
                text_record_object_code +=object_code
                text_record_length += len(object_code)
            else:
                text_record += (hex(len(text_record_object_code))[2:]+text_record_object_code)
                object_file.write("\n"+text_record)
                text_record = 'T'+ '0'*2+line[0:5]
                text_record_length = 0
                text_record_object_code = ""
        
                
                
        else:
            list_file.write(line.strip())
            end_record = 'E'+"0"*2+hex(int(start_add))[2:]
            object_file.write("\n"+end_record)
                
               
               
                    
    
    
    
    
            print(object_code)
            



    
    