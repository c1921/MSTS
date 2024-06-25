class Enemy:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power
        self.armor = 0

    def attack(self, player):
        attack_damage = self.attack_power
        damage_dealt = max(0, attack_damage - player.armor)
        player.hp -= damage_dealt
        player.armor = max(0, player.armor - attack_damage)
        return f'{self.name} attacked for {attack_damage} damage, dealing {damage_dealt} damage after armor!'

class Goblin(Enemy):
    def __init__(self):
        super().__init__('Goblin', 20, 6)

class Orc(Enemy):
    def __init__(self):
        super().__init__('Orc', 30, 8)

class Dragon(Enemy):
    def __init__(self):
        super().__init__('Dragon', 50, 12)
