from sys import exit

instruction_type={
    'add':'R',
    'sub':'R',
    'sll':'R',
    'slt':'R',
    'sltu':'R',
    'xor':'R',
    'srl':'R',
    'or':'R',
    'and':'R',
    'addi':'I',
    'lw':'I',
    'sltiu':'I',
    'jalr':'I',
    'sw':'S',
    'beq':'B',
    'bne':'B',
    'blt':'B',
    'bge':'B',
    'bltu':'B',
    'bgeu':'B',
    'lui':'U',
    'auipc':'U',
    'jal':'J'
}

Register_Encoding={
    'zero': '00000',
    'ra': '00001',
    'sp': '00010',
    'gp': '00011',
    'tp': '00100',
    't0': '00101',
    't1': '00110',
    't2': '00111',
    's0': '01000',
    'fp': '01000',
    's1': '01001',
    'a0': '01010',
    'a1': '01011',
    'a2': '01100',
    'a3': '01101',
    'a4': '01110',
    'a5': '01111',
    'a6': '10000',
    'a7': '10001',
    's2': '10010',
    's3': '10011',
    's4': '10100',
    's5': '10101',
    's6': '10110',
    's7': '10111',
    's8': '11000',
    's9': '11001',
    's10': '11010',
    's11': '11011',
    't3': '11100',
    't4': '11101',
    't5': '11110',
    't6': '11111',
}

OPCODES={
    'add':'0110011',
    'sub':'0110011',
    'sll':'0110011',
    'slt':'0110011',
    'sltu':'0110011',
    'xor':'0110011',
    'srl':'0110011',
    'or':'0110011',
    'and':'0110011',
    'addi':'0010011',
    'lw':'0000011',
    'sltiu':'0010011',
    'jalr':'1100111',
    'sw':'0100011',
    'beq':'1100011',
    'bne':'1100011',
    'blt':'1100011',
    'bge':'1100011',
    'bltu':'1100011',
    'bgeu':'1100011',
    'lui':'0110111',
    'auipc':'0010111',
    'jal':'1101111'
}


funct3={
    'add':'000',
    'sub':'000',
    'sll':'001',
    'slt':'010',
    'sltu':'011',
    'xor':'100',
    'srl':'101',
    'or':'110',
    'and':'111',
    'addi':'000',
    'lw':'010',
    'sltiu':'011',
    'jalr':'000',
    'sw':'010',
    'beq':'000',
    'bne':'001',
    'blt':'100',
    'bge':'101',
    'bltu':'110',
    'bgeu':'111'
}


funct7={
    'add':'0000000',
    'sub':'0100000',
    'sll':'0000000',
    'slt':'0000000',
    'sltu':'0000000',
    'xor':'0000000',
    'srl':'0000000',
    'or':'0000000',
    'and':'0000000'
}


label_table=dict()
global Address 
Address =0

# flag
halt_encountered = False  # This will be false until a hlt is enountered, if any instruction is encountered after the variable being true it'll throw an error

def remove_whitespace_and_empty_lines(input_filepath, output_filepath):
    # Read the content of the input file
    with open(input_filepath, 'r') as file:
        lines = file.readlines()

    # Remove leading white spaces and empty lines
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    # Write the cleaned lines to the output file
    with open(output_filepath, 'w') as file:
        file.write('\n'.join(cleaned_lines))

# Specify the full path to the input and output files
# input_filepath = "C:/Users/navsh/OneDrive/Desktop/sample.txt"
# output_filepath = 'C:/Users/navsh/OneDrive/Desktop/out.txt'

def string_to_n_bit_twos_complement_binary(n, input_string, location):
    try:
        input_integer = int(input_string)
    except ValueError:
        print(f'line {location}: ILLEGAL_IMMEDIATE: Not a valid integer.')
        terminate()

    min_value = -2**(n-1)
    max_value = 2**(n-1) - 1

    if not (min_value <= input_integer <= max_value):
        print(f"line {location}: OUT_OF_BOUND: Input integer out of range for {n}-bit two's complement.")
        print(f"Allowed range: [{min_value}, {max_value}]")
        terminate()

    if input_integer < 0:
        # For negative numbers, use 2's complement representation
        input_binary = bin((1 << n) + input_integer)[2:]
    else:
        input_binary = bin(input_integer)[2:]

    input_binary = input_binary.zfill(n)

    return input_binary

def terminate():
    exit(0)
    
def is_a_label(line):
    is_label=False
    for i in line:
        if i == ":":
            is_label=True
    return is_label

def decimal_to_hexadecimal(decimal_num):
    # Using the built-in format() function to convert decimal to formatted hexadecimal
    hex_value = format(decimal_num, '08x')
    
    return f'0x{hex_value}'

global location
location=decimal_to_hexadecimal(Address)

def go_down_line_by_line(line):
    global Address
    if is_a_label(line)==True:
        label_name = line.split(":")[0]
        if label_name in label_table:
            print(f'line {location}: ILLEGAL_LABEL: {label_name} already a label')
            terminate()
        label_table[label_name] = location
        x=len(label_name)
        line=line[x+1:]
        go_down_line_by_line(line)
        
    elif halt_encountered:
        if line =="beq,zero,zero,0":
            Address +=4
        else:
            print(f'line {location}: ILLEGAL_COMMAND: HALT already encountered')
            terminate()
    else:
        check_instruction_type(line,location)
        Address +=4
        
def no_error_in_register_name(register,location):
    if register not in Register_Encoding.keys():
        print(f'line {location}: ILLEGAL_REGISTER_ERROR: {register} not a valid register. ')
        terminate()

def no_error_in_label_name(name,location): 
    if name not in label_table:
        print(f'line {location}: UNDECLARED_LABEL: {name} used without declaration')
        terminate()
        
def check_instruction_type(line,location):
    list1=line.split()
    the_type=instruction_type[list1[0]]
    if the_type== 'R':
        return R_Type_Encoding(line,location)
    elif the_type== 'I':
        return I_Type_Encoding(line,location)
    elif the_type== 'B':
        return B_Type_Encoding(line,location)
    elif the_type== 'S':
        return S_Type_Encoding(line,location)
    elif the_type== 'U':
        return U_Type_Encoding(line,location)
    elif the_type== 'J':
        return J_Type_Encoding(line,location)
    else:
        print(f'line {location}: ILLEGAL_INSTRUCTION_ERROR: {list1[0]} not a valid instruction. ')
        
    
def R_Type_Encoding(line,location):
    #    [31: 25]     [24:20]     [19:15]     [14: 12]     [11:7]     [6:0]
    
    #     funct7        rs2         rs1        funct3        rd       opcode
    
    list1= line.split()
    list2= list1[1].split(',')
    list3=[]
    list3.append(list1[0])
    for i in list2:
        list3.append(i)
    #list3's first element is the instruction (add,sub,and,etc) according to which we will extract our opcode,funct7 and funct3
    #list3's second,third and fourth value are the rd,rs1 and rs2 registers whose encoding we find out from register encoding disctionary
    
    # We first check if the registers are valid or not
    no_error_in_register_name(list3[1],location)
    no_error_in_register_name(list3[2],location)
    no_error_in_register_name(list3[3],location)
    
    INSTRUCTION=list3[0] 
    FUNCT7= funct7[INSTRUCTION]
    FUNCT3=funct3[INSTRUCTION]
    OPCODE=OPCODES[INSTRUCTION]
    #FUNCT7,FUNCT3 and OPCODE are the funct7,funct3 and opcode corresponding to the instruction
    rd=Register_Encoding[list3[1]]
    rs1=Register_Encoding[list3[2]]
    rs2=Register_Encoding[list3[3]]
    #rd,rs1,rs2 are the binary encodings of the given registers
    binary_answer= FUNCT7+rs2+rs1+FUNCT3+rd+OPCODE
    return binary_answer
    
    
def S_Type_Encoding(line,location):
    #    [31:25]     [24:20]    [19:15]    [14: 12]    [11:7]    [6:0]
    
    #   imm[11:5]      rs2        rs1       funct3    imm[4:0]   opcode 
    
    
    #sw ra,32(sp)
    list1=line.split()
    list2= list1[1].split(',')
    list3=list2[1].split('(')
    list4=[]
    list4.append(list1[0])
    list4.append(list2[0])
    list4.append(list3[0])
    element=list3[1][:-1]
    list4.append(element)
    #now my list4 contains first element as instruction sw, thn second element as rs2, third element as immediate value and foruth value as the rs1

    INSTRUCTION=list4[0]
    FUNCT3=funct3[INSTRUCTION]
    OPCODE=OPCODES[INSTRUCTION]
    #FUNCT3 and OPCODE are the funct3 and opcode corresponding to the instruction
    no_error_in_register_name(list4[1],location)
    no_error_in_register_name(list4[3],location)
    #checking for errors in reg name
    rs2=Register_Encoding[list4[1]]
    rs1=Register_Encoding[list4[3]]
    #rs1,rs2 are the binary encodings of the given registers
    IMM=list4[2]
    IMMEDIATE=string_to_n_bit_twos_complement_binary(12,IMM,location)
    binary_answer= IMMEDIATE[11:5]+rs2+rs1+FUNCT3+IMMEDIATE[4:0]+OPCODE
    return binary_answer

def I_Type_Encoding(line,location):
    #[31:20]     [19:15]    [14:12]    [11:7]   [6:0]
   
    #imm[11:0]     rs1       funct3      rd     opcode
    
    #"lw a5,20(s1)"
    
    list1 = line.split()
    INSTRUCTION = list1[0]
    list2=list1[1].split(",")
    reg = list2[0]
    OPCODE=OPCODES[INSTRUCTION]
    FUNCT3 = funct3[INSTRUCTION]
    if list1[0] == 'lw':
        list3 = list2[1].split('(')
        list4 = [INSTRUCTION,reg,list3[0],list3[1][:-1]]
        imm = string_to_n_bit_twos_complement_binary(12,list4[2],location)
        rd=Register_Encoding[list4[1]]
        rs1=Register_Encoding[list4[3]]
        no_error_in_register_name(list4[1],location)
        no_error_in_register_name(list4[3],location)

    else:
        list2 = list1[1].split(',')
        list3 = []
        list3.append(list1[0])
        for i in list2:
            list3.append(i)

        rd = Register_Encoding[list3[1]]
        rs1 = Register_Encoding[list3[2].rstrip(',')]
        imm = string_to_n_bit_twos_complement_binary(12,list3[3],location)
        no_error_in_register_name(list3[1],location)
        no_error_in_register_name(list3[2],location)
    binary_answer= imm+rd+FUNCT3+rs1+OPCODE
    return binary_answer
    


def B_Type_Encoding(line, location):
    list1 = line.split()
    list2 = list1[1].split(',')
  
    INSTRUCTION = list1[0]
    FUNCT3 = funct3[INSTRUCTION]
    OPCODE = OPCODES[INSTRUCTION]

    no_error_in_register_name(list2[1], location)
    no_error_in_register_name(list2[0], location)

    rs2 = Register_Encoding[list2[1]]
    rs1 = Register_Encoding[list2[0]]

    IMM = list2[2]
    IMMEDIATE = string_to_n_bit_twos_complement_binary(13, IMM, location)

    binary_answer = IMMEDIATE[0] + IMMEDIATE[2:8] + rs2 + rs1 + FUNCT3 + IMMEDIATE[8:11] + IMMEDIATE[-1] + IMMEDIATE[1] + OPCODE
    return binary_answer
def U_Type_Encoding(line,location) : 

    #  [31:12]    [11:7]   [6:0]

    # imm[31:12]    rd     opcode

        list1= line.split()
        list2= list1[1].split(',')
        list3=[]
        list3.append(list1[0])
        for i in list2:
            list3.append(i)
    #list3 first element is lui or auipc
    #list3 2nd element is rd and 3rd element is the immediate value
        no_error_in_register_name(list3[1],location)
        INSTRUCTION = list3[0]
        OPCODE=OPCODES[INSTRUCTION]
        RD= Register_Encoding[list3[1]]
        IMM = list3[2]
        IMMEDIATE = string_to_n_bit_twos_complement_binary(32,IMM,location)
        binary_answer = IMMEDIATE[11:31]+RD+OPCODE
        return binary_answer


def J_Type_Encoding(line, location):
    #         [31:12]         [11:7]    [6:0]
    
    # imm[20|10:1|11|19:12]     ra      opcode

    list1 = line.split()
    INSTRUCTION = list1[0]
    list2 = list1[1].split(",")
    reg = list2[0]
    OPCODE = OPCODES[INSTRUCTION]
    # FUNCT3 = funct3[INSTRUCTION]
    if ')' in list1[1]:
        list3 = list2[1].split('(')
        list4=[]
        list4.append(INSTRUCTION)
        list4.append(reg)
        list4.append(list3[0])
        list4.append(list3[1][:-1])
        IMMEDIATE = string_to_n_bit_twos_complement_binary(21, list4[2], location)
        rd = Register_Encoding[list4[1]]
        
        no_error_in_register_name(list4[1], location)
        no_error_in_register_name(list4[3], location)
        binary_answer = IMMEDIATE[0]+IMMEDIATE[10:20]+IMMEDIATE[9]+IMMEDIATE[1:9] + rd + OPCODE 
        return binary_answer
        
    else:
        list1 = line.split()
        list2 = list1[1].split(',')
        list3 = []
        list3.append(list1[0])
        for i in list2:
            list3.append(i)
    
        INSTRUCTION = list3[0]
    
        OPCODE = OPCODES[INSTRUCTION]
        # OPCODE is the opcode corresponding to the instruction
        ra = Register_Encoding[list3[1]]
    
        # ra are the binary encodings of the given registers
        IMM = list3[2]
        IMMEDIATE = string_to_n_bit_twos_complement_binary(21,IMM, 1)
        binary_answer = IMMEDIATE[0]+IMMEDIATE[10:20]+IMMEDIATE[9]+IMMEDIATE[1:9] + ra + OPCODE 
        return binary_answer



def copy_file(input_file, output_file):
    try:
        # Open input file in read mode and output file in write mode
        with open(input_file, 'r') as assembly:
         
            # Read content from input file

            
            
            with open(assembly_strip, 'r') as main,open(output_file, 'w') as machine_code:
                r_assembly_strip = main.readlines()
                
                for i in r_assembly_strip:
                    
                    insert = go_down_line_by_line(i)
                    
                    machine_code.write(insert+'\n')
            
    except FileNotFoundError:
        print("File not found.")

# Test the function
input_file = input("Enter the path to the assembly file: ")   # Provide the path to your input file
assembly_strip = input("Enter the path to the text file: ")
remove_whitespace_and_empty_lines(input_file,assembly_strip)
output_file = input("Enter the path to the machine code file: ")  # Provide the path to your output file
copy_file(assembly_strip, output_file)
