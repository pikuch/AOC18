
class Group:
    def __init__(self, description, current_side, side_counter, boost):
        words = description.split()
        self.army = current_side
        self.name = "ImSys" + str(side_counter) if current_side == 0 else "Infec" + str(side_counter)
        self.count = int(words[0])
        self.hp = int(words[4])
        self.attack = int(words[-6]) + boost * (1 - current_side)
        self.attack_type = words[-5]
        self.initiative = int(words[-1])
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

    def load_data(self, data, boost):
        lines = data.split("\n")
        current_side = 0
        side_counter = [0] * 2
        for line in lines:
            if line == "Immune System:":
                current_side = 0
                continue
            if line == "Infection:":
                current_side = 1
                continue
            if line == "":
                continue
            side_counter[current_side] += 1
            self.groups.append(Group(line, current_side, side_counter[current_side], boost))

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
        targets = [group for group in self.groups if group.count > 0 and group.army != attacker.army and not group.chosen]
        targets.sort(key=lambda a: (self.get_damage(attacker, a), a.count * a.attack, a.initiative), reverse=True)

        # for t in targets:
        #     print(f"{attacker.name} would deal {t.name} {self.get_damage(attacker, t)} damage")

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
        # print(f"{attacker.name} attacks {defender.name} killing {kill_count}")
        return kill_count

    def run(self):
        killed_this_round = 1
        while self.get_army_units(0) and self.get_army_units(1) and killed_this_round:

            killed_this_round = 0

            # target selection phase
            attackers = [group for group in self.groups if group.count > 0]
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
                    killed_this_round += self.solve_attack(attacker, defender)

        return self.get_army_units(0), self.get_army_units(1)
