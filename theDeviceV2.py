def is_jump(linked, current):
    if linked == current:
        return " [JUMP]"
    else:
        return ""


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

    def translate(self):
        translation = [f"pc = r{self.pc_link}"]
        for i in range(len(self.program)):
            inst = self.program[i]
            if inst[0] == "addr":
                translation.append(f"{i:02d}: r{inst[3]} = r{inst[1]} + r{inst[2]}{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "addi":
                translation.append(f"{i:02d}: r{inst[3]} = r{inst[1]} + {inst[2]}{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "mulr":
                translation.append(f"{i:02d}: r{inst[3]} = r{inst[1]} * r{inst[2]}{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "muli":
                translation.append(f"{i:02d}: r{inst[3]} = r{inst[1]} * {inst[2]}{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "banr":
                translation.append(f"{i:02d}: r{inst[3]} = r{inst[1]} & r{inst[2]}{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "bani":
                translation.append(f"{i:02d}: r{inst[3]} = r{inst[1]} & {inst[2]}{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "borr":
                translation.append(f"{i:02d}: r{inst[3]} = r{inst[1]} | r{inst[2]}{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "bori":
                translation.append(f"{i:02d}: r{inst[3]} = r{inst[1]} | {inst[2]}{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "setr":
                translation.append(f"{i:02d}: r{inst[3]} = r{inst[1]}{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "seti":
                translation.append(f"{i:02d}: r{inst[3]} = {inst[1]}{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "gtir":
                translation.append(f"{i:02d}: IF {inst[1]} > r{inst[2]} THEN r{inst[3]} = 1 ELSE r{inst[3]} = 0{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "gtri":
                translation.append(f"{i:02d}: IF r{inst[1]} > {inst[2]} THEN r{inst[3]} = 1 ELSE r{inst[3]} = 0{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "gtrr":
                translation.append(f"{i:02d}: IF r{inst[1]} > r{inst[2]} THEN r{inst[3]} = 1 ELSE r{inst[3]} = 0{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "eqir":
                translation.append(f"{i:02d}: IF {inst[1]} == r{inst[2]} THEN r{inst[3]} = 1 ELSE r{inst[3]} = 0{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "eqri":
                translation.append(f"{i:02d}: IF r{inst[1]} == {inst[2]} THEN r{inst[3]} = 1 ELSE r{inst[3]} = 0{is_jump(self.pc_link, inst[3])}")
            elif inst[0] == "eqrr":
                translation.append(f"{i:02d}: IF r{inst[1]} == r{inst[2]} THEN r{inst[3]} = 1 ELSE r{inst[3]} = 0{is_jump(self.pc_link, inst[3])}")
            else:
                translation.append(f"{i:02d}: UNKNOWN INSTRUCTION: {str(inst)}")
        return translation

    def run(self):
        reg_1_values = set()
        last_reg_1 = 0

        while 0 <= self.pc < len(self.program):
            inst = self.program[self.pc]
            if inst[0] == "eqrr":
                print(f"\r{len(reg_1_values)}", end="")
                if self.reg[1] in reg_1_values:
                    print(last_reg_1)
                    break
                else:
                    reg_1_values.add(self.reg[1])
                    last_reg_1 = self.reg[1]

            self.reg[self.pc_link] = self.pc
            self.ops[inst[0]](inst)
            self.pc = self.reg[self.pc_link]
            self.pc += 1
