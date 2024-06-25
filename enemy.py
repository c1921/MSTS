class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.armor = 0
        self.damage = damage

    def attack(self, player):
        if player.armor > 0:
            absorbed = min(player.armor, self.damage)
            player.armor -= absorbed
            player.hp -= (self.damage - absorbed)
            return f'{self.name} attacks {player.name} for {self.damage} damage! {absorbed} damage absorbed by armor!'
        else:
            player.hp -= self.damage
            return f'{self.name} attacks {player.name} for {self.damage} damage!'
