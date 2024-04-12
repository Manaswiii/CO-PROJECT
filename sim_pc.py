from sim_converter import *

class ProgramCounter:
    PC = "" # the value stored here is in binary

    def __init__(self, val):
        self.PC = format(val, "08b")

    def getVal(self):
        return self.PC
    
    def update(self, val):
        self.PC = val

    def dump(self):
        print(self.PC, end=" ")
