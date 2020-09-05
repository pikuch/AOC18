import numpy as np


class Entity:
    def __init__(self, tp, row, col):
        self.type = tp
        self.hp = 200   # health points
        self.ap = 3     # attack points
        self.row = row
        self.col = col


class Cave:
    def __init__(self, data):
        lines = data.split("\n")
        self.WALL = -1
        self.ELF = -11
        self.GOBLIN = -12
        self.elves = []
        self.goblins = []
        self.caves = np.zeros((len(lines), len(lines[0])), dtype=np.int32)
        for row in range(len(lines)):
            for col in range(len(lines[0])):
                if lines[row][col] == "#":
                    self.caves[row, col] = self.WALL
                elif lines[row][col] == "E":
                    self.caves[row, col] = self.ELF
                    self.elves.append(Entity("E", row, col))
                elif lines[row][col] == "G":
                    self.caves[row, col] = self.GOBLIN
                    self.goblins.append(Entity("G", row, col))

    def show(self):
        print("\n" * 80)
        for row in range(self.caves.shape[0]):
            line_end = "    "
            for col in range(self.caves.shape[1]):
                if self.caves[row, col] == self.WALL:
                    print("░░░", end="")
                elif self.caves[row, col] == self.ELF:
                    print(" E ", end="")
                    for elf in self.elves:
                        if elf.row == row and elf.col == col:
                            line_end += "  E(" + str(elf.hp) + ")"
                            break
                elif self.caves[row, col] == self.GOBLIN:
                    print(" G ", end="")
                    for gob in self.goblins:
                        if gob.row == row and gob.col == col:
                            line_end += "  G(" + str(gob.hp) + ")"
                            break
                else:
                    print(" · ", end="")
            print(line_end)
