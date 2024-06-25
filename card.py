class Card:
    def __init__(self, name, cost, damage, block, description, card_type):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.block = block
        self.description = description
        self.card_type = card_type  # 卡片类型：攻击牌、技能牌、能力牌

    def play(self, player, enemy, last_card=None):
        extra_damage = 0
        if last_card and self.card_type == 'Attack' and last_card.card_type == 'Attack':
            extra_damage = 5
        if player.energy >= self.cost:
            player.energy -= self.cost
            enemy.hp -= (self.damage + extra_damage)
            player.armor += self.block
            return f'{player.name} used {self.name} ({self.card_type}) on {enemy.name}, dealing {self.damage + extra_damage} damage and gaining {self.block} block!'
        else:
            return f'Not enough energy to play {self.name}!'
