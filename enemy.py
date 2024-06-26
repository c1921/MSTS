class Enemy:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power
        self.armor = 0
        self.poison = 0
        self.states = {}  # 状态属性

    def attack(self, player):
        attack_damage = self.attack_power
        damage_dealt = max(0, attack_damage - player.armor)
        player.hp -= damage_dealt
        player.armor = max(0, player.armor - attack_damage)
        return f'{self.name} attacked for {attack_damage} damage, dealing {damage_dealt} damage after armor!'

    def add_state(self, state_name, amount):
        if state_name in self.states:
            self.states[state_name] += amount
        else:
            self.states[state_name] = amount

    def remove_state(self, state_name, amount):
        if state_name in self.states:
            self.states[state_name] -= amount
            if self.states[state_name] <= 0:
                del self.states[state_name]

class Goblin(Enemy):
    def __init__(self):
        super().__init__('Goblin', 20, 6)

class Orc(Enemy):
    def __init__(self):
        super().__init__('Orc', 30, 8)

class Dragon(Enemy):
    def __init__(self):
        super().__init__('Dragon', 50, 12)
