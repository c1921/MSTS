from card import Card

# 定义卡牌
strike = Card('Strike', 1, 6, 0, 'Deal 6 damage.', 'Attack')
defend = Card('Defend', 1, 0, 5, 'Gain 5 block.', 'Skill')
fireball = Card('Fireball', 2, 10, 0, 'Deal 10 damage.', 'Attack')
combo_strike = Card('Combo Strike', 1, 5, 0, 'Deal 5 damage. If the last played card was an Attack, deal 5 extra damage.', 'Attack')

# 所有种类的卡片列表
all_cards = [strike, defend, fireball, combo_strike]
