def I_Type_Encoding(line):
    #[31:20]     [19:15]    [14:12]    [11:7]   [6:0]
   
    #imm[11:0]     rs1       funct3      rd     opcode

    if OPCODE == 'lw':
        list1 = line.split()
        op = list1[0]
        desr = list1[1]
        im_sr = list1[2]
        im , sr = im_sr[:-1].split('(')
        list3 = [op,desr,im,sr]
        
        INSTRUCTION = list3[0]
        FUNCT3 = funct3[INSTRUCTION]
        OPCODE=OPCODES[INSTRUCTION]
        imm = binary(list3[2])
        rd=Register_Encoding[list3[1]]
        rs1=Register_Encoding[list3[3]]
        binary_answer= imm+rd+FUNCT3+rs1+OPCODE
        print(binary_answer)

    else:
        list1= line.split()
        list2= list1[1].split(',')



or 
def I_Type_Encoding(line):
    global OPCODE
    global Address

    if halt_encountered:
        print(f'ILLEGAL_COMMAND: HALT already encountered')
        terminate()

    # Move the assignment before the conditional statement
    INSTRUCTION = line.split()[0]
    OPCODE = OPCODES[INSTRUCTION]

    if OPCODE == 'lw':
        list1 = line.split()
        op = list1[0]
        desr = list1[1]

        # Extract immediate value and register from the operand
        im_sr = list1[2].rstrip(')').split(',')
        im, sr = im_sr[0], im_sr[1]

        list3 = [op, desr, im, sr]

        FUNCT3 = funct3[INSTRUCTION]
        imm = binary(list3[2])
        rd = Register_Encoding[list3[1]]
        rs1 = Register_Encoding[list3[3]]
        binary_answer = imm + rs1 + FUNCT3 + rd + OPCODE  # Corrected order
        print(binary_answer)

    else:
        list1 = line.split()
        list2 = list1[1].split(',')
        list3 = []
        list3.append(list1[0])
        for i in list2:
            list3.append(i)

        FUNCT3 = funct3[INSTRUCTION]
        rd = Register_Encoding[list3[1]]
        rs1 = Register_Encoding[list3[2].rstrip(',')]
        imm = binary(list3[3])
        binary_answer = imm + rs1 + FUNCT3 + rd + OPCODE  # Corrected order
        print(binary_answer)


I_Type_Encoding("lw a5,20(s1)")

        list3=[]
        list3.append(list1[0])
        for i in list2:
            list3.append(i)
    
        INSTRUCTION = list3[0]
        FUNCT3 = funct3[INSTRUCTION]
        OPCODE=OPCODES[INSTRUCTION]
        rd=Register_Encoding[list3[1]]
        rs1=Register_Encoding[list3[2]]
        imm = binary(list3[3])
        binary_answer= imm+rd+FUNCT3+rs1+OPCODE
        print(binary_answer)
I_Type_Encoding(jalr ra,a5,-07)
I_Type_Encoding(lw a5,20(s1))
