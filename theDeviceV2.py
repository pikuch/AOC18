
class DeviceV2:
    def __init__(self):
        self.reg = [0] * 6
        self.pc = 0
        self.pc_link = None
        self.program = []
        self.ops = {"addr": self.addr, "addi": self.addi,
                    "mulr": self.mulr, "muli": self.muli,
                    "banr": self.banr, "bani": self.bani,
                    "borr": self.borr, "bori": self.bori,
                    "setr": self.setr, "seti": self.seti,
                    "gtir": self.gtir, "gtri": self.gtri, "gtrr": self.gtrr,
                    "eqir": self.eqir, "eqri": self.eqri, "eqrr": self.eqrr}

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
            words = line.split()
            if words[0] == "#ip":
                self.pc_link = int(words[1])
            else:
                for i in range(1, len(words)):
                    words[i] = int(words[i])
                self.program.append(words)

    def run(self):
        while 0 <= self.pc < len(self.program):
            inst = self.program[self.pc]
            self.reg[self.pc_link] = self.pc
            self.ops[inst[0]](inst)
            self.pc = self.reg[self.pc_link]
            self.pc += 1
