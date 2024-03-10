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
    'sltui':'I',
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
    'sltui':'0010011',
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
    'sltui':'011',
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
# flag
halt_encountered = False  # This will be false until a hlt is enountered, if any instruction is encountered after the variable being true it'll throw an error


def binary(num):  # converts any integer into 12 bit binary representation, only valid for 12 bit numbers, i.e. 0 to 4096
    return "{:012b}".format(num)


def terminate():
    exit(0)
    
def go_down_line_by_line(line,location):
    global Address
    if not line:
        return
    elif line[-1] == ':':
        label_name = line[:-1].lstrip()
        if label_name in label_table:
            print(f'line {location}: ILLEGAL_LABEL: {label_name} already a label')
            terminate()
        label_table[label_name] = Address
    elif halt_encountered:
        print(f'line {location}: ILLEGAL_COMMAND: HALT already encountered')
        terminate()
    else:
        check_instruction(line,location)
        Address +=1
        
def no_error_in_register_name(register,location):
    if register not in Register_Encoding.keys():
        print(f'line {location}: ILLEGAL_REGISTER_ERROR: {register} not a valid register. ')
        terminate()
    
def out_of_bound_length(value,location):
    if value<=0 or value>=4095:
        print(f'line {location}: OVERFLOW: {value} not in the range 0-4095')

def no_error_in_label_name(name,location): 
    if name not in label_table:
        print(f'line {location}: UNDECLARED_LABEL: {name} used without declaration')
        terminate()
        
