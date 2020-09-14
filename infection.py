
class Group:
    def __init__(self, description, current_side):
        words = description.split()
        self.army = current_side
        self.count = int(words[0])
        self.hp = int(words[4])
        self.attack = int(words[-6])
        self.attack_type = words[-5]
        self.initiative = words[-1]
        self.weak = []
        self.immune = []
        self.chosen = False
        if words[7][0] == "(":
            parameters = words[7:-11]
            current_property = self.weak
            for p in parameters:
                p = p.strip(",;()")
                if p == "weak":
                    current_property = self.weak
                    continue
                if p == "immune":
                    current_property = self.immune
                    continue
                if p == "to":
                    continue
                current_property.append(p)


class Infection:
    def __init__(self):
        self.groups = []

    def load_data(self, data):
        lines = data.split("\n")
        current_side = 0
        for line in lines:
            if line == "Immune System:":
                current_side = 0
                continue
            if line == "Infection:":
                current_side = 1
                continue
            if line == "":
                continue
            self.groups.append(Group(line, current_side))

    def get_army_units(self, n):
        counter = 0
        for group in self.groups:
            if group.army == n:
                counter += group.count
        return counter

    def get_damage(self, attacker, target):
        if attacker.attack_type in target.immune:
            return 0
        effective_power = attacker.count * attacker.attack
        if attacker.attack_type in target.weak:
            effective_power *= 2
        return effective_power

    # choose a suitable target from enemies
    def choose_target(self, attacker):
        targets = [group for group in self.groups if group.count and group.army != attacker.army and not group.chosen]
        targets.sort(key=lambda a: (self.get_damage(attacker, a), a.count * a.attack, a.initiative), reverse=True)
        if len(targets) == 0:
            return None
        if self.get_damage(attacker, targets[0]) == 0:
            return None
        else:
            targets[0].chosen = True
            return targets[0]

    def solve_attack(self, attacker, defender):
        if attacker.attack_type in defender.immune:
            damage = 0
        else:
            damage = attacker.count * attacker.attack
            if attacker.attack_type in defender.weak:
                damage *= 2
        kill_count = damage // defender.hp
        if defender.count - kill_count < 0:
            kill_count = defender.count
        defender.count -= kill_count
        # print(f" killed {kill_count},", end="")

    def run(self):
        while self.get_army_units(0) and self.get_army_units(1):
            # target selection phase
            attackers = [group for group in self.groups if group.count]
            attackers.sort(key=lambda a: (a.count * a.attack, a.initiative), reverse=True)
            fights = []
            for group in self.groups:   # reset chosen groups
                group.chosen = False
            for attacker in attackers:
                fights.append((attacker, self.choose_target(attacker)))

            # attack phase
            fights.sort(key=lambda a: a[0].initiative, reverse=True)
            for attacker, defender in fights:
                if attacker.count and defender is not None:
                    self.solve_attack(attacker, defender)
        return self.get_army_units(0), self.get_army_units(1)
