instruction_type = {
    'add': 'R',
    'sub': 'R',
    'sll': 'R',
    'slt': 'R',
    'sltu': 'R',
    'xor': 'R',
    'srl': 'R',
    'or': 'R',
    'and': 'R',
    'addi': 'I',
    'lw': 'I',
    'sltiu': 'I',
    'jalr': 'I',
    'sw': 'S',
    'beq': 'B',
    'bne': 'B',
    'blt': 'B',
    'bge': 'B',
    'bltu': 'B',
    'bgeu': 'B',
    'lui': 'U',
    'auipc': 'U',
    'jal': 'J'
}

Register_Encoding = {
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

OPCODES = {
    'add': '0110011',
    'sub': '0110011',
    'sll': '0110011',
    'slt': '0110011',
    'sltu': '0110011',
    'xor': '0110011',
    'srl': '0110011',
    'or': '0110011',
    'and': '0110011',
    'addi': '0010011',
    'lw': '0000011',
    'sltiu': '0010011',
    'jalr': '1100111',
    'sw': '0100011',
    'beq': '1100011',
    'bne': '1100011',
    'blt': '1100011',
    'bge': '1100011',
    'bltu': '1100011',
    'bgeu': '1100011',
    'lui': '0110111',
    'auipc': '0010111',
    'jal': '1101111'
}

funct3 = {
    'add': '000',
    'sub': '000',
    'sll': '001',
    'slt': '010',
    'sltu': '011',
    'xor': '100',
    'srl': '101',
    'or': '110',
    'and': '111',
    'addi': '000',
    'lw': '010',
    'sltiu': '011',
    'jalr': '000',
    'sw': '010',
    'beq': '000',
    'bne': '001',
    'blt': '100',
    'bge': '101',
    'bltu': '110',
    'bgeu': '111'
}

funct7 = {
    'add': '0000000',
    'sub': '0100000',
    'sll': '0000000',
    'slt': '0000000',
    'sltu': '0000000',
    'xor': '0000000',
    'srl': '0000000',
    'or': '0000000',
    'and': '0000000'
}

def sext(value, bits):
    
    if value & (1 << (bits - 1)):
        return value - (1 << bits)
    else:
        return value
def unsigned(value, bits):
    return value & ((1 << bits) - 1)

def execute_r_type(instruction, rd, rs1, rs2, registers):
    opcode = OPCODES[instruction]
    funct3_val = funct3[instruction]
    funct7_val = funct7[instruction]

    if rd not in Register_Encoding or rs1 not in Register_Encoding or rs2 not in Register_Encoding:
        raise ValueError("Invalid register number")

    if instruction == "add":
        registers[rd] = registers[rs1] + registers[rs2]
    elif instruction == "sub":
        registers[rd] = registers[rs1] - registers[rs2]
    elif instruction == "sll":
        registers[rd] = registers[rs1] << (registers[rs2] & 0b11111)
    elif instruction == "slt":
        registers[rd] = 1 if registers[rs1] < registers[rs2] else 0
    elif instruction == "sltu":
        registers[rd] = 1 if (registers[rs1] & 0xFFFFFFFF) < (registers[rs2] & 0xFFFFFFFF) else 0
    elif instruction == "xor":
        registers[rd] = registers[rs1] ^ registers[rs2]
    elif instruction == "srl":
        registers[rd] = registers[rs1] >> (registers[rs2] & 0b11111)
    elif instruction == "or":
        registers[rd] = registers[rs1] | registers[rs2]
    elif instruction == "and":
        registers[rd] = registers[rs1] & registers[rs2]
    else:
        raise ValueError("Unsupported R-type instruction")

def execute_i_type(instruction, rd, rs1, imm, registers, memory):
    opcode = OPCODES[instruction]
    funct3_val = funct3[instruction]

    if rd not in Register_Encoding or rs1 not in Register_Encoding:
        raise ValueError("Invalid register number")

    if instruction == "addi":
        registers[rd] = registers[rs1] + imm
    elif instruction == "lw":
        address = registers[rs1] + imm
        registers[rd] = memory[address]
    elif instruction == "sltiu":
        registers[rd] = 1 if registers[rs1] < imm else 0
    elif instruction == "jalr":
        registers[rd] = pc + 4
        pc = registers[rs1] + imm
    else:
        raise ValueError("Unsupported I-type instruction")
        
def execute_b_type(instruction,rs1,rs2,imm,pc):
    opcode = OPCODES[instruction]
    funct3_val = func3[instruction]
    if rs1 not in Register_encoding or rs2 not in Register_Encoding:
        raise ValueError("Invalid register number")

    if instruction == "beq":
         offset = (imm << 1) | 0b0
         target_address = pc + offset
         if rs1 == rs2:  
            return target_address, True  
         else:
            return pc + 4, False
    if instruction == "bne":
         offset = (imm << 1) | 0b0  
         target_address = pc + offset  
        
         if rs1 != rs2:  
            return target_address, True  
         else:
            return pc + 4, False

    if instruction == "blt":
        offset = (imm << 1) | 0b0  
        target_address = pc + offset 
        if sext(rs1, 32) >= sext(rs2, 32):
            return pc + 4, False
        else:
            return target_address, True
    if instruction == "bltu":
        offset = (imm << 1) | 0b0  
        target_address = pc + offset 
        if unsigned(rs1, 32) >= unsigned(rs2, 32):
            return pc + 4, False
        else:
            return target_address, True

    if instruction == "bge":
        offset = (imm << 1) | 0b10  
        target_address = pc + offset 
        if sext(rs1, 32) < sext(rs2, 32):
            return pc + 4, False
        else:
            return target_address, True

    if instruction == "bgeu": 
        offset = (imm << 1) | 0b0  
        target_address = pc + offset 
        if unsigned(rs1, 32) < unsigned(rs2, 32):
            return pc + 4, False
        else:
            return target_address, True 

def decode_instruction(instruction):
    opcode = instruction & 0b1111111

    for inst, opcode_value in OPCODES.items():
        if opcode_value == opcode:
            return inst

    return "Unknown"

def execute_instruction(instruction, rd, rs1, rs2, registers, memory):
    instruction_type = instruction_type[decode_instruction(instruction)]
    if instruction_type == "R":
        execute_r_type(instruction, rd, rs1, rs2, registers)
    elif instruction_type == "I":
        execute_i_type(instruction, rd, rs1, imm, registers, memory)
    elif instruction_type == "B":
        execute_b_type(instruction,rs1,rs2,imm,pc)
    # Implement handling for other instruction types as needed

def output_machine_state(pc, registers, memory):
    pc_str = format(pc, '032b')

    register_values = [registers.get(f"x{i}", 0) for i in range(32)]
    registers_str = ' '.join(format(val, '032b') for val in register_values)

    memory_str = ""
    for address in range(32):
        memory_str += format(memory.get(address, 0), '032b') + '\n'

    output = f"{pc_str} {registers_str}\n{memory_str}"

    return output

