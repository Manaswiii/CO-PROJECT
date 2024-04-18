#INPUT FILE AND ITS CONTENT ADDED IN A LIST OF LINES


f = open("in.txt", "r")
lines = f.readlines()
if not lines:
    print("Error: Input file is empty")
    exit()


for line in lines:
    line = line.strip()
num_lines = len(lines)
#    print(line)
    
# print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")


#***********************************************************************************************************


#DICTIONARIES USED IN THE SIMULATOR


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

Register_value={
'00000': 0 ,
'00001': 0 ,
'00010': 0 ,
'00011': 0 ,
'00100': 0 ,
'00101': 0 ,
'00110': 0 ,
'00111': 0 ,
'01000': 0 ,
'01001': 0 ,
'01010': 0 ,
'01011': 0 ,
'01100': 0 ,
'01101': 0 ,
'01110': 0 ,
'01111': 0 ,
'10000': 0 ,
'10001': 0 ,
'10010': 0 ,
'10011': 0 ,
'10100': 0 ,
'10101': 0 ,
'10110': 0 ,
'10111': 0 ,
'11000': 0 ,
'11001': 0 ,
'11010': 0 ,
'11011': 0 ,
'11100': 0 ,
'11101': 0 ,
'11110': 0 ,
'11111': 0 
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

OPCODE_to_instruction_type={
    '0110011':'R',
    '0000011':'I',
    '0010011':'I',
    '1100111':'I',
    '0100011':'S',
    '1100011': 'B',
    '0110111':'U',
    '0010111':'U',
    '1101111':'J'
}

# funct3={
#     'add':'000',
#     'sub':'000',
#     'sll':'001',
#     'slt':'010',
#     'sltu':'011',
#     'xor':'100',
#     'srl':'101',
#     'or':'110',
#     'and':'111',
#     'addi':'000',
#     'lw':'010',
#     'sltiu':'011',
#     'jalr':'000',
#     'sw':'010',
#     'beq':'000',
#     'bne':'001',
#     'blt':'100',
#     'bge':'101',
#     'bltu':'110',
#     'bgeu':'111'
# }


# funct7={
#     'add':'0000000',
#     'sub':'0100000',
#     'sll':'0000000',
#     'slt':'0000000',
#     'sltu':'0000000',
#     'xor':'0000000',
#     'srl':'0000000',
#     'or':'0000000',
#     'and':'0000000'
# }

MEMORY={
    '0x00010000' :0,
    '0x00010004' :0,
    '0x00010008':0,
    '0x0001000c':0,
    '0x00010010':0,
    '0x00010014':0,
    '0x00010018':0,
    '0x0001001c':0,
    '0x00010020':0,
    '0x00010024':0,
    '0x00010028':0,
    '0x0001002c':0,
    '0x00010030':0,
    '0x00010034':0,
    '0x00010038':0,
    '0x0001003c':0,
    '0x00010040':0,
    '0x00010044':0,
    '0x00010048':0,
    '0x0001004c':0,
    '0x00010050':0,
    '0x00010054':0,
    '0x00010058':0,
    '0x0001005c':0,
    '0x00010060':0,
    '0x00010064':0,
    '0x00010068':0,
    '0x0001006c':0,
    '0x00010070':0,
    '0x00010074':0,
    '0x00010078':0,
    '0x0001007c':0
}


num_lines = len(lines)
PC = {}

for i in range(0, num_lines * 4, 4):
    line_index = i // 4
    line = lines[line_index]
    PC[i] = line
if not PC:
    print("Error: PC dictionary is empty")
    exit()

#********************************************************************************************************

#OPENING FILE FOR OUTPUT IN WRITE MODE

OUTPUTS=[]
r=open("out.txt",'w')

#*********************************************************************************************************

#FUNCTIONS USED IN THE CODE

def dec_to_bin_32(num):
    binary = bin(num)[2:]
    binary = binary.zfill(32)
    return binary

def binary_to_decimal(binary_str):
    # Convert binary string to decimal integer using int() function with base 2
    decimal_value = int(binary_str, 2)
    return (decimal_value)

def sext(value, bits):
    if int(value) & (1 << (bits - 1)):
        return int(value) - (1 << bits)
    else:
        return int(value)
    
def unsigned(value, bits):
    return int(value) & ((1 << bits) - 1)

def execute_r_type(instruction, rd, rs1, rs2,func3,func7):
    if func3=='000' and func7=='0000000': #instruction == "add":
        Register_value[rd] = Register_value[rs1] + Register_value[rs2]
    elif func3=='000' and func7=='0100000':#instruction == "sub":
        Register_value[rd] = Register_value[rs1] - Register_value[rs2]
    elif func3=='001' and func7=='0000000': #instruction == "sll":
        Register_value[rd] = Register_value[rs1] << (Register_value[rs2] & 0b11111)
    elif func3=='010' and func7=='0000000': #instruction == "slt":
        Register_value[rd] = 1 if Register_value[rs1] < Register_value[rs2] else 0
    elif func3=='011' and func7=='0000000': #instruction == "sltu":
        Register_value[rd] = 1 if (Register_value[rs1] & 0xFFFFFFFF) < (Register_value[rs2] & 0xFFFFFFFF) else 0
    elif func3=='100' and func7=='0000000': #instruction == "xor":
        Register_value[rd] = Register_value[rs1] ^ Register_value[rs2]
    elif func3=='101' and func7=='0000000': #instruction == "srl":
        Register_value[rd] = Register_value[rs1] >> (Register_value[rs2] & 0b11111)
    elif func3=='110' and func7=='0000000': #instruction == "or":
        Register_value[rd] = Register_value[rs1] | Register_value[rs2]
    elif func3=='111' and func7=='0000000': #instruction == "and":
        Register_value[rd] = Register_value[rs1] & Register_value[rs2]
    else:
        raise ValueError("Unsupported R-type instruction")

def execute_i_type(instruction, rd, rs1, immediate,func3,opcode,PC_Execution):
    imm=binary_to_decimal(immediate)
    if func3=='000' and opcode=='0010011': #instruction == "addi":
        Register_value[rd] = Register_value[rs1] + imm
    elif func3 == '010' and opcode == '0000011':  # instruction == "lw":
        address_decimal = Register_value[rs1] + imm
        address_hex = hex(address_decimal)  # Convert decimal address to hexadecimal
        # Access memory using hexadecimal address
        Register_value[rd] = MEMORY.get(address_hex, 0)
    elif func3=='011' and opcode=='0010011': #instruction == "sltiu":
        Register_value[rd] = 1 if Register_value[rs1] < imm else 0
    elif func3=='000' and opcode=='1100111': #instruction == "jalr":
        Register_value[rd] = PC_Execution + 4
        PC_Execution = Register_value[rs1] + imm
    else:
        raise ValueError("Unsupported I-type instruction")
        
def execute_b_type(instruction,rs1,rs2,immediate,func3,PC_Execution):
    imm=binary_to_decimal(immediate)
    if  func3 =="000":
        offset = sext(immediate,12)
         
        if Register_value[rs1 ]==Register_value[rs2]:  
            PC_Execution += offset
         
    if  func3 =="001":
        offset = sext(immediate,12)  
           
        
        if Register_value[rs1] != Register_value[rs2]:  
            PC_Execution += offset  
         

    if  func3 =="100":
        offset = sext(immediate,12)  
        
        if sext(Register_value[rs1], 32) < sext(Register_value[rs2], 32):
            PC_Execution += offset

    if  func3 =="110":
        offset = sext(immediate,12)  
        
        if unsigned(Register_value[rs1], 32) < unsigned(Register_value[rs2], 32):
            PC_Execution += offset

    if  func3 =="101":
        offset = sext(immediate,12)  
        
        if sext(Register_value[rs1], 32) >= sext(Register_value[rs2], 32):
            PC_Execution += offset

    if  func3 =="111":
        offset = sext(immediate,12)  
        
        if unsigned(Register_value[rs1], 32) >= unsigned(Register_value[rs2], 32):
            PC_Execution += offset

def execute_s_type(instruction,rs2,rs1,immediate,func3,opcode,PC_Execution):
    imm = binary_to_decimal(immediate)
    if func3 == "010":
            address = Register_value[rs1] + sext(imm,32)

    # Store the value in register rs2 to memory at the calculated address
            MEMORY[address] = Register_value[rs2]
         
    else:
        raise ValueError("Unsupported S-type instruction")
    
def execute_u_type(instruction,  rd, imm, opcode, PC_Execution):
    imm_decimal = binary_to_decimal(imm)
    if opcode=="0110111": #instruction = lui
        Register_value[rd] = imm_decimal << 12
    elif opcode=="0010111":
        Register_value[rd] = PC_Execution + (imm_decimal << 12)
    else:
        raise ValueError("Unsupported U-type instruction")


def execute_j_type(instruction, rd, imm, opcode, PC_Execution):
    imm_decimal = binary_to_decimal(imm)
    Register_value[rd] = PC_Execution + 4
    offset = ((int(imm) & 0b111111111111) << 1) | 0b0
    target_address = PC_Execution + offset
    target_address &= 0xFFFFFFFE
    PC_Execution = target_address
    
    
def PC_AND_ALL_REGS_OUTPUT(PC_Execution):
    output = '0b'+ str(dec_to_bin_32(PC_Execution)) + " " 
    register_bin_values = {}  # Dictionary to store binary values for each register key
    
    for key, value in Register_value.items():
        register_bin_values[key] = dec_to_bin_32(value)  
        output += "0b" + register_bin_values[key] + ' '
    output+='\n'
    OUTPUTS.append(output)
    
    return register_bin_values

def MEMORY_OUTPUT():
    MEMORY_bin_values = {} 
     # Dictionary to store binary values for each memory key
    for key, value in MEMORY.items():
        
        MEMORY_bin_values[key] = dec_to_bin_32(value)  
        out = str(key) + ": " + "0b" + MEMORY_bin_values[key] +'\n'
           # Construct the output string for each key-value pair
        r.write(out)

def Decode_Instruction_Type(instruction):
    OPCODE=instruction[-8:-1]
    INSTRUCTION_TYPE=OPCODE_to_instruction_type[OPCODE]
    return INSTRUCTION_TYPE

def execute_instruction(instruction,PC_Execution):
    types = Decode_Instruction_Type(instruction)
    if types == "R":
        execute_r_type(instruction, instruction[20:25], instruction[12:17], instruction[7:12],instruction[17:20],instruction[0:7])
        #print("R",instruction[20:25]," ",instruction[12:17]," ",instruction[7:12]," ",instruction[17:20]," ",instruction[0:7])
    elif types == "I":
        execute_i_type(instruction, instruction[20:25], instruction[12:17], instruction[0:12],instruction[17:20],instruction[25:32],PC_Execution)
        #print("I",instruction[20:25]," ",instruction[12:17]," ",binary_to_decimal(instruction[0:12])," ",instruction[17:20]," ",instruction[25:32])
    elif types == "B":
        imm=instruction[0]+instruction[24]+instruction[1:7]+instruction[20:26]
        execute_b_type(instruction,instruction[12:17],instruction[20:25],imm,instruction[17:20],PC_Execution)
        #print("B",instruction[12:17]," ",instruction[20:25]," ",binary_to_decimal(imm)," ",instruction[17:20]," ",instruction[0:7])
    elif types == "S":
        imm = instruction[0:7] + instruction[20:25]
        execute_s_type(instruction, instruction[7:12], instruction[12:17], imm, instruction[17:20],instruction[25:31],PC_Execution)
    elif types == "U":
        execute_u_type(instruction,instruction[20:25],instruction[0:20],instruction[25:32],PC_Execution)
    elif types == "J":
        imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11]
        execute_j_type(instruction,instruction[20:25],imm,instruction[25:32],PC_Execution)
    return types
    # Implement handling for other instruction types as needed
    
# def Execute(line,PC):
#     #Get instruction_type
#     #Write functions for each instruction type like R_type(line,PC) in which we take our output and add it in a string and then add the string to OUTPUT list
#     #for every instructions take PC as a parameter besides line like B_type(line,L,PC)
#     #TIn functions that manipulate the PC should change inside the function and append its output in the OUTPUT list like any other type
#     #WE WILL HAVE TO ADD /n AT THE END OF EVERY OUTPUT
#     return
      

#*********************************************************************************************************

# PC IMPLEMENTATION AND ACTUAL EXECTUTION OF THE SIMULATOR


PC_end = max(PC.keys())
PC_Execution = 4  # Start PC_Execution from 0

while PC_Execution < PC_end:
    instruction = PC[PC_Execution]  
    execute_instruction(instruction, PC_Execution)
    PC_AND_ALL_REGS_OUTPUT(PC_Execution)
    PC_Execution += 4

        

for i in OUTPUTS:
    r.write(i)
MEMORY_OUTPUT()
f.close()
r.close()
