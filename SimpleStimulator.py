#INPUT FILE AND ITS CONTENT ADDED IN A LIST OF LINES
import sys

f = open(sys.argv[1], "r")
lines = f.readlines()
if not lines:
    print("Error: Input file is empty")
    exit()

for line in lines:
    line = line.strip()
num_lines = len(lines)
#    print(line)
    
# print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")


#*************


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

for i in range(4, num_lines * 4, 4):
    line_index = (i // 4 )-1
    line = lines[line_index]
    PC[i] = line
if not PC:
    print("Error: PC dictionary is empty")
    exit()

#************

#OPENING FILE FOR OUTPUT IN WRITE MODE

OUTPUTS=[]
r=open(sys.argv[2],'w')

#*************

#FUNCTIONS USED IN THE CODE

def hex_to_decimal(hex_string):
    # Remove the '0x' prefix if present
    hex_string = hex_string[2:] if hex_string.startswith('0x') else hex_string
    # Convert hexadecimal string to decimal
    decimal_value = int(hex_string, 16)
    return decimal_value

def decimal_to_hex(decimal):
    # Convert the decimal number to hexadecimal
    hex_value = hex(decimal & 0xFFFFFFFF)  # Mask with 0xFFFFFFFF to ensure only 32 bits are considered
    # Ensure the hex value has at least 8 characters (excluding '0x')
    hex_value = hex_value[2:].zfill(8)
    # Convert the hex string to a list of characters
    hex_list = list(hex_value)
    # Set the 5th bit from the right (index 4) to 1
    hex_list[-5] = '1'
    # Construct the 32-bit hexadecimal representation
    hex_representation = "0x" + ''.join(hex_list)
    return hex_representation

def dec_to_bin_32(num):
    num = int(num)
    if num < 0:
        positive_binary = bin(-num)[2:]
        positive_binary = positive_binary.zfill(31)
        # Invert the bits
        inverted_bits = ''.join('0' if bit == '1' else '1' for bit in positive_binary)
        # Add 1
        binary = bin(int(inverted_bits, 2) + 1)[2:]
    else:
        binary = bin(num)[2:]
        binary = binary.zfill(32)
    return binary


def unsigned_binary_to_decimal(binary_str):
    decimal_value = int(binary_str, 2)
    return decimal_value

def signed_binary_to_decimal(binary_str):
    if binary_str[0] == '0': 
        return unsigned_binary_to_decimal(binary_str)
    else:
        flipped_bits = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        decimal_value = unsigned_binary_to_decimal(flipped_bits) + 1
        return -decimal_value


def sext(value, bits):
    if int(value) & (1 << (bits - 1)):
        return int(value) - (1 << bits)
    else:
        return int(value)
    
def unsigned(value, bits):
    return int(value) & ((1 << bits) - 1)
def add(rd, rs1, rs2):
    # Convert register values to binary
    rs1_binary = dec_to_bin_32(rs1)
    rs2_binary = dec_to_bin_32(rs2)
    
    # Convert binary values to decimal
    rs1_decimal = signed_binary_to_decimal(rs1_binary)
    rs2_decimal = signed_binary_to_decimal(rs2_binary)
    
    # Perform addition
    result_decimal = rs1_decimal + rs2_decimal
    
    # Convert the result back to binary
    result_binary = dec_to_bin_32(result_decimal)
    
    # Store the result in the destination register
    Register_value[rd] = result_decimal

def sub(rd, rs1, rs2):
    # Special case: sub rd, x0, rs
    if rd == '00000':
        Register_value[rs2] = -Register_value[rs2]  # Negate the value in register rs2
    
    # Convert register values to binary
    rs1_binary = dec_to_bin_32(rs1)
    rs2_binary = dec_to_bin_32(rs2)
    
    # Convert to signed binary
    rs1_signed = sext(rs1_binary, 32)
    rs2_signed = sext(rs2_binary, 32)
    
    # Perform subtraction
    result_binary = bin(rs1_signed - rs2_signed)[2:].zfill(32)
    
    # Convert binary result back to decimal
    result_decimal = signed_binary_to_decimal(result_binary)
    
    # Store the result in the destination register
    Register_value[rd] = result_decimal

def slt(rd, rs1, rs2):
    # Convert register values to binary
    rs1_binary = dec_to_bin_32(rs1)
    rs2_binary = dec_to_bin_32(rs2)
    
    # Sign-extend the binary values
    rs1_signed = sext(rs1_binary, 32)
    rs2_signed = sext(rs2_binary, 32)
    
    # Perform signed comparison
    if rs1_signed < rs2_signed:
        Register_value[rd] = 1

def sltu(rd, rs1, rs2):
    # Convert register values to binary
    rs1_binary = dec_to_bin_32(rs1)
    rs2_binary = dec_to_bin_32(rs2)
    
    # Perform unsigned comparison
    if unsigned_binary_to_decimal(rs1_binary) < unsigned_binary_to_decimal(rs2_binary):
        Register_value[rd] = 1

def xor(rd, rs1, rs2):
    # Convert register values to binary
    rs1_binary = dec_to_bin_32(rs1)
    rs2_binary = dec_to_bin_32(rs2)
    
    # Perform bitwise XOR operation
    result_binary = bin(rs1_binary - rs2_binary)[2:].zfill(32)
    
    # Convert binary result back to decimal
    result_decimal = unsigned_binary_to_decimal(result_binary)
    
    # Store the result in the destination register
    Register_value[rd] = result_decimal

def sll(rd, rs1, rs2):
    # Perform logical left shift
    shift_amount = unsigned_binary_to_decimal(rs2[-5:])
    result_decimal = Register_value[rs1] << shift_amount
    
    # Store the result in the destination register
    Register_value[rd] = result_decimal

def srl(rd, rs1, rs2):
    # Perform logical right shift
    shift_amount = unsigned_binary_to_decimal(rs2[-5:])
    result_decimal = Register_value[rs1] >> shift_amount
    
    # Store the result in the destination register
    Register_value[rd] = result_decimal

def _or(rd, rs1, rs2):
    # Perform bitwise OR operation
    result_decimal = Register_value[rs1] | Register_value[rs2]
    
    # Store the result in the destination register
    Register_value[rd] = result_decimal

def _and(rd, rs1, rs2):
    # Perform bitwise AND operation
    result_decimal = Register_value[rs1] & Register_value[rs2]
    
    # Store the result in the destination register
    Register_value[rd] = result_decimal


def execute_r_type(instruction, rd, rs1, rs2,func3,func7):
    if func3=='000' and func7=='0000000': #instruction == "add":
        add(rd,rs1,rs2)
    elif func3=='000' and func7=='0100000':#instruction == "sub":
        sub(rd,rs1,rs2)
    elif func3=='001' and func7=='0000000': #instruction == "sll":
        sll(rd,rs1,rs2)
    elif func3=='010' and func7=='0000000': #instruction == "slt":
        slt(rd,rs1,rs2)
    elif func3=='011' and func7=='0000000': #instruction == "sltu":
        sltu(rd,rs1,rs2)
    elif func3=='100' and func7=='0000000': #instruction == "xor":
        xor(rd,rs1,rs2)
    elif func3=='101' and func7=='0000000': #instruction == "srl":
        srl(rd,rs1,rs2)
    elif func3=='110' and func7=='0000000': #instruction == "or":
        _or(rd,rs1,rs2)
    elif func3=='111' and func7=='0000000': #instruction == "and":
        _and(rd,rs1,rs2)
    else:
        raise ValueError("Unsupported R-type instruction")
    
def lw(rd, rs1, imm):
    address = Register_value[rs1] + sext(imm, 12)
    address_hex = decimal_to_hex(address)  # Convert decimal address to hexadecimal
    data = MEMORY[address_hex]
    binary_data = dec_to_bin_32(data)
    Register_value[rd] = unsigned_binary_to_decimal(binary_data)

def addi(rd, rs, imm):
    rs_value = dec_to_bin_32(Register_value[rs])
    imm_value = dec_to_bin_32(sext(imm, 12))
    result_binary = bin(int(rs_value, 2) + int(imm_value, 2))[2:].zfill(32)
    Register_value[rd] = signed_binary_to_decimal(result_binary)

def sltiu(rd, rs, imm):
    rs_value = dec_to_bin_32(Register_value[rs])
    imm_value = dec_to_bin_32(sext(imm, 12))
    if unsigned_binary_to_decimal(rs_value) < unsigned_binary_to_decimal(imm_value):
        Register_value[rd] = 1
    else:
        Register_value[rd] = 0

def jalr(rd, rs, offset):
    rs_value = dec_to_bin_32(Register_value[rs])
    offset_value = dec_to_bin_32(sext(offset, 12))
    PC_Execution = signed_binary_to_decimal(rs_value) + signed_binary_to_decimal(offset_value)
    Register_value[rd] = PC + 4
    return PC_Execution & 0xFFFFFFFE  # Ensure LSB of PC is 0


def execute_i_type(instruction, rd, rs1, immediate,func3,opcode,PC_Execution):
    if func3=='000' and opcode=='0010011': #instruction == "addi":
        addi(rd,rs1,immediate)
    elif func3 == '010' and opcode == '0000011':  # instruction == "lw":
        lw(rd,rs1,immediate)
    elif func3=='011' and opcode=='0010011': #instruction == "sltiu":
        sltiu(rd,rs1,immediate)
    elif func3=='000' and opcode=='1100111': #instruction == "jalr":
        jalr(rd,rs1,immediate)
    else:
        raise ValueError("Unsupported I-type instruction")
    
def execute_b_type(instruction, rs1, rs2, immediate, func3, PC_Execution):
    # offset = signed_binary_to_decimal(immediate)
    offset = str(sext(int(immediate, 2),32))
    offset = signed_binary_to_decimal(offset)

    if func3 == "000" and Register_value[rs1] == Register_value[rs2]:
        PC_Execution += offset
        # print(offset)
        # print (PC_Execution)

    elif func3 == "001" and Register_value[rs1] != Register_value[rs2]:
        PC_Execution += offset
        # print(offset)
        # print (PC_Execution)

    elif func3 == "100" and Register_value[rs1] < Register_value[rs2]:
        PC_Execution += offset
        # print(offset)
        # print (PC_Execution)

    elif func3 == "110" and Register_value[rs1] >= Register_value[rs2]:
        PC_Execution += offset
        # print(offset)
        # print (PC_Execution)

    elif func3 == "101" and signed_binary_to_decimal(rs1) < signed_binary_to_decimal(rs2):
        PC_Execution += offset
        # print(offset)
        # print (PC_Execution)

    elif func3 == "111" and signed_binary_to_decimal(rs1) >= signed_binary_to_decimal(rs2):
        PC_Execution += offset
        # print(offset)
        # print (PC_Execution)

    return PC_Execution

        
# def execute_b_type(instruction,rs1,rs2,immediate,func3,PC_Execution):
#     imm=signed_binary_to_decimal(immediate)
#     offset=0
#     if  func3 =="000":
#         offset = sext(immediate,12)
         
#         if Register_value[rs1 ]==Register_value[rs2]:  
#             PC_Execution += offset
#             print(type(offset))
         
#     if  func3 =="001":
#         offset = sext(immediate,12)  
#         print(type(offset))
#         if Register_value[rs1] != Register_value[rs2]:  
#             PC_Execution += offset  
         

#     if  func3 =="100":
#         offset = sext(immediate,12)  
        
#         if sext(Register_value[rs1], 32) < sext(Register_value[rs2], 32):
#             PC_Execution += offset
#             print(type(offset))

#     if  func3 =="110":
#         offset = sext(immediate,12)  
#         print(type(offset))

#         if unsigned(Register_value[rs1], 32) < unsigned(Register_value[rs2], 32):
#             PC_Execution += offset

#     if  func3 =="101":
#         offset = sext(immediate,12)  
#         print(type(offset))
        
#         if sext(Register_value[rs1], 32) >= sext(Register_value[rs2], 32):
#             PC_Execution += offset

#     if  func3 =="111":
#         offset = sext(immediate,12)  
#         print(type(offset))
        
#         if unsigned(Register_value[rs1], 32) >= unsigned(Register_value[rs2], 32):
#             PC_Execution += offset
#     print(offset)

def execute_s_type(instruction, rs2, rs1, immediate, func3, opcode, PC_Execution):
    imm = signed_binary_to_decimal(immediate)
    if func3 == "010":
        address = decimal_to_hex(Register_value[rs1] + imm)

        # Store the value in register rs2 to memory at the calculated address
        MEMORY[address] = Register_value[rs2]
    else:
        raise ValueError("Unsupported S-type instruction")


def execute_u_type(instruction, rd, imm, opcode, PC_Execution):
    imm_decimal = signed_binary_to_decimal(imm)
    if opcode == "0110111":  # lui
        # Convert the immediate value to binary
        imm_binary = dec_to_bin_32(imm_decimal)
        # Left shift by 12 bits (equivalent to multiplying by 4096)
        result_binary = imm_binary + '0' * 12
        # Convert the binary result back to decimal
        result_decimal = unsigned_binary_to_decimal(result_binary)
        # Store the result in the destination register
        Register_value[rd] = result_decimal
    elif opcode == "0010111":  # auipc
        # Compute the address
        address_decimal = PC_Execution + (imm_decimal)
        # Convert the address to binary
        address_binary = dec_to_bin_32(address_decimal)
        # Convert the binary address back to decimal
        address_decimal = decimal_to_hex(unsigned_binary_to_decimal(address_binary))
        # Store the address in the destination register
        Register_value[rd] = address_decimal
    else:
        raise ValueError("Unsupported U-type instruction")


def execute_j_type(instruction, rd, imm, opcode, PC_Execution):
    imm_decimal = signed_binary_to_decimal(imm)
    # Store the return address in register rd
    Register_value[rd] = PC_Execution + 4
    # Calculate the target address
    target_address = PC_Execution + (imm_decimal)
    # Ensure that the LSB of the target address is 0
    target_address &= 0xFFFFFFFE
    
    # Convert the target address to binary
    target_address_binary = dec_to_bin_32(target_address)
    
    # Convert binary target address back to decimal
    target_address_decimal = signed_binary_to_decimal(target_address_binary)
    
    # Update the program counter
    PC_Execution = target_address_decimal

    
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
        #print(key," :" ,value,"/n")
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
        #print(PC_Execution, " R",instruction[20:25]," ",instruction[12:17]," ",instruction[7:12]," ",instruction[17:20]," ",instruction[0:7])
    elif types == "I":
        execute_i_type(instruction, instruction[20:25], instruction[12:17], instruction[0:12],instruction[17:20],instruction[25:32],PC_Execution)
        #print(PC_Execution, " I",instruction[20:25]," ",instruction[12:17]," ",signed_binary_to_decimal(instruction[0:12])," ",instruction[17:20]," ",instruction[25:32])
    elif types == "B":
        imm=instruction[0]+instruction[24]+instruction[1:7]+instruction[20:26]
        PC_Execution=execute_b_type(instruction,instruction[12:17],instruction[20:25],imm,instruction[17:20],PC_Execution)
        #print(PC_Execution, " B",instruction[12:17]," ",instruction[20:25]," ",signed_binary_to_decimal(imm)," ",instruction[17:20]," ",instruction[0:7])
    elif types == "S":
        imm = instruction[0:7] + instruction[20:25]
        execute_s_type(instruction, instruction[7:12], instruction[12:17], imm, instruction[17:20],instruction[25:31],PC_Execution)
        #print(PC_Execution, " S",instruction[7:12]," ",instruction[12:17]," ",signed_binary_to_decimal(imm)," ",instruction[17:20]," ",instruction[25:31])
    elif types == "U":
        execute_u_type(instruction,instruction[20:25],instruction[0:20],instruction[25:32],PC_Execution)
        #print(PC_Execution, " U",instruction[20:25]," ",instruction[0:20]," ",signed_binary_to_decimal(instruction[0:20])," ",instruction[25:32])
    elif types == "J":
        imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11]
        execute_j_type(instruction,instruction[20:25],imm,instruction[25:32],PC_Execution)
        #print(PC_Execution, " J",instruction[20:25]," ",instruction[0:20]," ",signed_binary_to_decimal(imm)," ",instruction[25:32])
    return types
    # Implement handling for other instruction types as needed
    
# def Execute(line,PC):
#     #Get instruction_type
#     #Write functions for each instruction type like R_type(line,PC) in which we take our output and add it in a string and then add the string to OUTPUT list
#     #for every instructions take PC as a parameter besides line like B_type(line,L,PC)
#     #TIn functions that manipulate the PC should change inside the function and append its output in the OUTPUT list like any other type
#     #WE WILL HAVE TO ADD /n AT THE END OF EVERY OUTPUT
#     return
      

#*************

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
