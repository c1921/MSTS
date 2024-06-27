class Card:
    def __init__(self, name, description, card_type, cost):
        self.name = name
        self.description = description
        self.card_type = card_type
        self.cost = cost

    def play(self, player, enemy, last_played_card):
        pass

class Strike(Card):
    def __init__(self):
        super().__init__('Strike', 'Deal 6 damage.', 'Attack', 1)

    def play(self, player, enemy, last_played_card):
        if player.energy < self.cost:
            return 'Not enough energy to play Strike!'
        player.energy -= self.cost
        damage_dealt = max(0, 6 - enemy.armor)
        enemy.hp -= damage_dealt
        return f'Hero used Strike on {enemy.name}, dealing {damage_dealt} damage!'

class Defend(Card):
    def __init__(self):
        super().__init__('Defend', 'Gain 5 block.', 'Skill', 1)
        self.armor_gain = 5

    def play(self, player, enemy, last_played_card):
        if player.energy < self.cost:
            return 'Not enough energy to play Defend!'
        player.energy -= self.cost
        player.armor += self.armor_gain
        return f'Hero used Defend, gaining {self.armor_gain} block!'

class Fireball(Card):
    def __init__(self):
        super().__init__('Fireball', 'Deal 10 damage.', 'Attack', 2)

    def play(self, player, enemy, last_played_card):
        if player.energy < self.cost:
            return 'Not enough energy to play Fireball!'
        player.energy -= self.cost
        damage_dealt = max(0, 10 - enemy.armor)
        enemy.hp -= damage_dealt
        return f'Hero used Fireball on {enemy.name}, dealing {damage_dealt} damage!'

class ComboStrike(Card):
    def __init__(self):
        super().__init__('Combo Strike', 'Deal 5 damage. If the last played card was an Attack, deal 5 extra damage.', 'Attack', 1)

    def play(self, player, enemy, last_played_card):
        if player.energy < self.cost:
            return 'Not enough energy to play Combo Strike!'
        player.energy -= self.cost
        base_damage = 5
        if last_played_card and last_played_card.card_type == 'Attack':
            base_damage += 5
        damage_dealt = max(0, base_damage - enemy.armor)
        enemy.hp -= damage_dealt
        return f'Hero used Combo Strike on {enemy.name}, dealing {damage_dealt} damage!'

# 新的卡牌设计
class Heal(Card):
    def __init__(self):
        super().__init__('Heal', 'Heal 10 HP.', 'Skill', 2)

    def play(self, player, enemy, last_played_card):
        if player.energy < self.cost:
            return 'Not enough energy to play Heal!'
        player.energy -= self.cost
        player.hp = min(player.max_hp, player.hp + 10)
        return 'Hero used Heal, recovering 10 HP!'

class ShieldBash(Card):
    def __init__(self):
        super().__init__('Shield Bash', 'Deal 5 damage and gain 5 block.', 'Attack', 1)

    def play(self, player, enemy, last_played_card):
        if player.energy < self.cost:
            return 'Not enough energy to play Shield Bash!'
        player.energy -= self.cost
        player.armor += 5
        damage_dealt = max(0, 5 - enemy.armor)
        enemy.hp -= damage_dealt
        return f'Hero used Shield Bash on {enemy.name}, dealing {damage_dealt} damage and gaining 5 block!'

class Poison(Card):
    def __init__(self):
        super().__init__('Poison', 'Deal 4 damage and apply 3 poison.', 'Skill', 1)

    def play(self, player, enemy, last_played_card):
        if player.energy < self.cost:
            return 'Not enough energy to play Poison!'
        player.energy -= self.cost
        damage_dealt = max(0, 4 - enemy.armor)
        enemy.hp -= damage_dealt
        enemy.add_state('Poison', 3)  # 添加毒性状态
        return f'Hero used Poison on {enemy.name}, dealing {damage_dealt} damage and applying 3 poison!'

# 将所有卡牌添加到列表中
all_cards = [Strike(), Defend(), Fireball(), ComboStrike(), Heal(), ShieldBash(), Poison()]
