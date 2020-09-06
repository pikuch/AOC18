import numpy as np
from collections import deque


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
            if mob.row == row and mob.col == col and mob.hp:
                return mob

    def show(self):
        _ = input()
        print("\n" * 80)
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

    # return a set of all squares that are next to enemies
    def get_set_of_empty_squares_next_to_enemies(self, actor):
        enemy = "G" if actor.type == "E" else "E"
        squares = set()
        for m in self.mobs:
            if m.hp and m.type == enemy:
                for r, c in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                    if self.caves[m.row + r, m.col + c] == 0:
                        squares.add((m.row + r, m.col + c))
        return squares

    # get only the closest spots from the set
    def get_closest_spots(self, start_row, start_col, spots):
        closest_spots = []
        closest_spot_distance = None
        visited = set()
        visited.add((start_row, start_col))
        to_check = deque()
        to_check.append((start_row, start_col, 0))
        while len(to_check):
            row, col, moves = to_check.popleft()
            # check if it's one of the spots we are looking for
            if (row, col) in spots:
                spots.remove((row, col))
                if len(closest_spots) == 0:  # the first found spot
                    closest_spots.append((row, col))
                    closest_spot_distance = moves
                else:  # maybe a spot at the same distance
                    if closest_spot_distance == moves:
                        closest_spots.append((row, col))
                    else:
                        return closest_spots
            # consider surrounding points
            for r, c in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                if self.caves[row + r, col + c] == 0 and (row + r, col + c) not in visited:
                    to_check.append((row + r, col + c, moves + 1))
                    visited.add((row + r, col + c))

        return closest_spots

    # step closer to one of the enemies, if possible
    def move_to_enemies(self, actor, attack_spots):
        closest_spots = self.get_closest_spots(actor.row, actor.col, attack_spots)
        if len(closest_spots) == 0:
            return
        if len(closest_spots) > 1:
            closest_spots.sort(key=lambda x: (x[0], x[1]))
        destination = closest_spots[0]
        # consider step options
        step_options = []
        for r, c in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            if self.caves[actor.row + r, actor.col + c] == 0:
                step_options.append((actor.row + r, actor.col + c))
        if len(step_options) > 1:
            step_options = self.get_closest_spots(destination[0], destination[1], set(step_options))
        if len(step_options) > 1:
            step_options.sort(key=lambda x: (x[0], x[1]))
        # finally move to step_options[0]
        self.caves[actor.row, actor.col] = 0
        actor.row, actor.col = step_options[0][0], step_options[0][1]
        self.caves[actor.row, actor.col] = self.GOBLIN if actor.type == "G" else self.ELF

    # attack or move and attack
    def act(self, actor):
        targets = self.get_close_enemies(actor)
        if len(targets) > 0:
            self.attack_from_list(actor, targets)
        else:
            attack_spots = self.get_set_of_empty_squares_next_to_enemies(actor)
            if len(attack_spots) == 0:
                return
            self.move_to_enemies(actor, attack_spots)
            targets = self.get_close_enemies(actor)
            if len(targets) > 0:
                self.attack_from_list(actor, targets)

    def run(self):
        while True:
            self.mobs.sort(key=lambda x: (x.row, x.col))
            for m in self.mobs:
                if m.hp:
                    if (m.type == "E" and self.goblin_count == 0) or (m.type == "G" and self.elf_count == 0):
                        return self.rounds * sum([mob.hp for mob in self.mobs])
                    self.act(m)
            self.rounds += 1
            self.show()
