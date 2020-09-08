
class DeviceV2:
    def __init__(self):
        self.reg = [0] * 6
        self.pc = 0
        self.program = []
        self.ops = {15: self.addr, 4: self.addi,
                    6: self.mulr, 5: self.muli,
                    11: self.banr, 8: self.bani,
                    12: self.borr, 10: self.bori,
                    2: self.setr, 0: self.seti,
                    3: self.gtir, 9: self.gtri, 7: self.gtrr,
                    1: self.eqir, 13: self.eqri, 14: self.eqrr}

    def addr(self, inst):
        self.reg[inst[3]] = self.reg[inst[1]] + self.reg[inst[2]]

    def addi(self, inst):
        self.reg[inst[3]] = self.reg[inst[1]] + inst[2]

    def mulr(self, inst):
        self.reg[inst[3]] = self.reg[inst[1]] * self.reg[inst[2]]

    def muli(self, inst):
        self.reg[inst[3]] = self.reg[inst[1]] * inst[2]

    def banr(self, inst):
        self.reg[inst[3]] = self.reg[inst[1]] & self.reg[inst[2]]

    def bani(self, inst):
        self.reg[inst[3]] = self.reg[inst[1]] & inst[2]

    def borr(self, inst):
        self.reg[inst[3]] = self.reg[inst[1]] | self.reg[inst[2]]

    def bori(self, inst):
        self.reg[inst[3]] = self.reg[inst[1]] | inst[2]

    def setr(self, inst):
        self.reg[inst[3]] = self.reg[inst[1]]

    def seti(self, inst):
        self.reg[inst[3]] = inst[1]

    def gtir(self, inst):
        self.reg[inst[3]] = 1 if inst[1] > self.reg[inst[2]] else 0

    def gtri(self, inst):
        self.reg[inst[3]] = 1 if self.reg[inst[1]] > inst[2] else 0

    def gtrr(self, inst):
        self.reg[inst[3]] = 1 if self.reg[inst[1]] > self.reg[inst[2]] else 0

    def eqir(self, inst):
        self.reg[inst[3]] = 1 if inst[1] == self.reg[inst[2]] else 0

    def eqri(self, inst):
        self.reg[inst[3]] = 1 if self.reg[inst[1]] == inst[2] else 0

    def eqrr(self, inst):
        self.reg[inst[3]] = 1 if self.reg[inst[1]] == self.reg[inst[2]] else 0

    def load(self, program):
        for line in program.split("\n"):
            self.program.append(tuple(map(int, line.split())))

    def run(self):
        for inst in self.program:
            self.ops[inst[0]](inst)
