import numpy as np


class Mob:
    def __init__(self, tp, row, col):
        self.type = tp
        self.hp = 200  # health points
        self.ap = 3  # attack points
        self.row = row
        self.col = col

    def __str__(self):
        return f"{self.type}[{self.hp}]"  # @{self.row},{self.col}"


class Cave:
    def __init__(self, data):
        lines = data.split("\n")
        self.rounds = 0
        self.WALL = -1
        self.ELF = -11
        self.GOBLIN = -12
        self.mobs = []
        self.elf_count = 0
        self.goblin_count = 0
        self.caves = np.zeros((len(lines), len(lines[0])), dtype=np.int32)
        for row in range(len(lines)):
            for col in range(len(lines[0])):
                if lines[row][col] == "#":
                    self.caves[row, col] = self.WALL
                elif lines[row][col] == "E":
                    self.caves[row, col] = self.ELF
                    self.mobs.append(Mob("E", row, col))
                    self.elf_count += 1
                elif lines[row][col] == "G":
                    self.caves[row, col] = self.GOBLIN
                    self.mobs.append(Mob("G", row, col))
                    self.goblin_count += 1

    # return the mob at (row, col)
    def get_mob_at(self, row, col):
        for mob in self.mobs:
            if mob.row == row and mob.col == col:
                return mob

    def show(self):
        # print("\n" * 80)
        for row in range(self.caves.shape[0]):
            line_end = "    "
            for col in range(self.caves.shape[1]):
                if self.caves[row, col] == self.WALL:
                    print("░░░", end="")
                elif self.caves[row, col] == self.ELF:
                    print(" E ", end="")
                    line_end += "  " + str(self.get_mob_at(row, col))
                elif self.caves[row, col] == self.GOBLIN:
                    print(" G ", end="")
                    line_end += "  " + str(self.get_mob_at(row, col))
                else:
                    print(" · ", end="")
            print(line_end)

    # return a list of enemy mobs next to a mob
    def get_close_enemies(self, mob):
        return [self.get_mob_at(mob.row + r, mob.col + c) for r, c in ((-1, 0), (0, -1), (0, 1), (1, 0))
                if (mob.type == "G" and self.caves[mob.row + r, mob.col + c] == self.ELF)
                or (mob.type == "E" and self.caves[mob.row + r, mob.col + c] == self.GOBLIN)]

    # attack one of the targets from the list
    def attack_from_list(self, actor, targets):
        # find the weakest target(s)
        weak_targets = []
        lowest_hp = 9**9
        for t in targets:
            if t.hp < lowest_hp:
                lowest_hp = t.hp
                weak_targets = [t]
            elif t.hp == lowest_hp:
                weak_targets.append(t)
        if len(weak_targets) > 1:
            weak_targets.sort(key=lambda x: (x.row, x.col))
        # attack weak_targets[0]
        if weak_targets[0].hp - actor.ap <= 0:  # kill
            weak_targets[0].hp = 0
            self.caves[weak_targets[0].row, weak_targets[0].col] = 0
            if weak_targets[0].type == "G":
                self.goblin_count -= 1
            else:
                self.elf_count -= 1
        else:  # hurt, not kill
            weak_targets[0].hp -= actor.ap

    def act(self, actor):
        targets = self.get_close_enemies(actor)
        if len(targets) > 0:
            self.attack_from_list(actor, targets)
        else:
            # TODO: move to targets if possible

            targets = self.get_close_enemies(actor)
            if len(targets) > 0:
                self.attack_from_list(actor, targets)

    def run(self):
        while self.rounds < 1:  # TODO: while True
            self.rounds += 1
            self.mobs.sort(key=lambda x: (x.row, x.col))
            for m in self.mobs:
                if m.hp:
                    if (m.type == "E" and self.goblin_count == 0) or (m.type == "G" and self.elf_count == 0):
                        return "No more enemies!"
                    self.act(m)
