def B_Type_Encoding(line,location):
    #    [31:25]     [24:20]    [19:15]    [14: 12]    [11:7]    [6:0]
    
    #   imm[12|10:5]      rs2        rs1       funct3    imm[4:1|11]   opcode 
    
    
    #blt a4,a5,label
    list1=line.split()
    list2= list1[1].split(',')
    

  
    #now my list4 contains first element as instruction blt, thn second element as rs2, third element as immediate value and foruth value as the rs1

    INSTRUCTION=list1[0]
    FUNCT3=funct3[INSTRUCTION]
    OPCODE=OPCODES[INSTRUCTION]
    #FUNCT3 and OPCODE are the funct3 and opcode corresponding to the instruction
    rs2=Register_Encoding[list2[1]]
    rs1=Register_Encoding[list2[0]]
    #rs1,rs2 are the binary encodings of the given registers
    IMM=list2[2]
    IMMEDIATE=string_to_12bit_twos_complement_binary(IMM,location)
    binary_answer= IMMEDIATE[0]+IMMEDIATE[2:8]+rs2+rs1+FUNCT3+IMMEDIATE[8:11]+IMMEDIATE[-1]+IMMEDIATE[1]+OPCODE
    print(binary_answer)
