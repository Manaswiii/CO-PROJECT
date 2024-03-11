def U_Type_Encoding(line,location) : 

    #imm[31:12] rd opcode 
    #[31:12] [11:7] [6:0]

    list1= line.split()
    list2= list1[1].split(',')
    list3=[]
    list3.append(list1[0])
    for i in list2:
        list3.append(i)
    #list3 first element is lui or auipc
    #list3 2nd element is rd and 3rd element is the immediate valye
    no_error_in_register_name(list3[1],location)
    no_error_in_register_name(list3[2],location)
    no_error_in_register_name(list3[3],location)

    INSTRUCTION = list3[0]

    if INSTRUCTION=="lui":  #check for the first element is auipc or lui 
        OPCODE=OPCODES[INSTRUCTION]
        RD= Register_Encoding[list3[1]]
        IMM = list[2]
        IMMEDIATE = string_to_12bit_twos_complement_binary(IMM,location)
        binary_answer = IMMEDIATE[31:12:-1]+RD+OPCODE
        print(binary_answers)

    if INSTRUCTION=="auipc":
        OPCODE=OPCODES[INSTRUCTION]
        RD= Register_Encoding[list3[1]]
        IMM = list[2]
        IMMEDIATE = string_to_12bit_twos_complement_binary(IMM,location)
        binary_answer = IMMEDIATE[31:12:-1]+RD+OPCODE
        print(binary_answers)
