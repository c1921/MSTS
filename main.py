import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox, QListWidget

class Card:
    def __init__(self, name, cost, damage, block, description, card_type):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.block = block
        self.description = description
        self.card_type = card_type  # 卡片类型：攻击牌、技能牌、能力牌

    def play(self, player, enemy):
        if player.energy >= self.cost:
            player.energy -= self.cost
            enemy.hp -= self.damage
            player.armor += self.block
            return f'{player.name} used {self.name} ({self.card_type}) on {enemy.name}, dealing {self.damage} damage and gaining {self.block} block!'
        else:
            return f'Not enough energy to play {self.name}!'

class Player:
    def __init__(self, name, hp, energy):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.energy = energy
        self.armor = 0
        self.hand = []
        self.deck = []
        self.discard_pile = []

    def draw_card(self):
        if not self.deck and self.discard_pile:
            self.deck = self.discard_pile[:]
            self.discard_pile.clear()
            random.shuffle(self.deck)

        if self.deck:
            card = self.deck.pop(0)
            self.hand.append(card)
            return f'{self.name} drew {card.name}'
        else:
            return 'Deck is empty!'

    def draw_cards(self, num):
        for _ in range(num):
            print(self.draw_card())

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

# 定义卡牌
strike = Card('Strike', 1, 6, 0, 'Deal 6 damage.', 'Attack')
defend = Card('Defend', 1, 0, 5, 'Gain 5 block.', 'Skill')
fireball = Card('Fireball', 2, 10, 0, 'Deal 10 damage.', 'Attack')

# 所有种类的卡片列表
all_cards = [strike, defend, fireball]

# 定义角色
player = Player('Hero', 30, 3)
enemy = Enemy('Slime', 20, 5)

# 初始化玩家的卡组
player.deck = [strike]*5 + [defend]*5 + [fireball]
random.shuffle(player.deck)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.player = player
        self.enemy = enemy
        self.initUI()
        self.start_player_turn()

    def initUI(self):
        self.setWindowTitle('Slay the Spire Clone')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # 显示游戏信息的标签
        self.info_label = QLabel('Welcome to the battle!')
        self.layout.addWidget(self.info_label)

        # 显示玩家能量的标签
        self.energy_label = QLabel(f'Energy: {self.player.energy}')
        self.layout.addWidget(self.energy_label)

        # 显示玩家HP和护甲的标签
        self.player_hp_label = QLabel(f'Player HP: {self.player.hp}/{self.player.max_hp} Armor: {self.player.armor}')
        self.layout.addWidget(self.player_hp_label)

        # 显示敌人HP和护甲的标签
        self.enemy_hp_label = QLabel(f'Enemy HP: {self.enemy.hp} Armor: {self.enemy.armor}')
        self.layout.addWidget(self.enemy_hp_label)

        # 显示玩家手牌的布局
        self.hand_layout = QHBoxLayout()
        self.layout.addLayout(self.hand_layout)

        # 显示抽牌堆的列表
        self.deck_list = QListWidget()
        self.layout.addWidget(QLabel('Deck:'))
        self.layout.addWidget(self.deck_list)

        # 显示弃牌堆的列表
        self.discard_pile_list = QListWidget()
        self.layout.addWidget(QLabel('Discard Pile:'))
        self.layout.addWidget(self.discard_pile_list)

        # 显示所有卡片种类的列表
        self.all_cards_list = QListWidget()
        for card in all_cards:
            self.all_cards_list.addItem(f'{card.name}: {card.description} ({card.card_type}) (Cost: {card.cost})')
        self.layout.addWidget(self.all_cards_list)

        # 结束回合的按钮
        self.end_turn_button = QPushButton('End Turn')
        self.end_turn_button.clicked.connect(self.end_turn)
        self.layout.addWidget(self.end_turn_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def update_hand(self):
        # 更新玩家手牌显示
        while self.hand_layout.count():
            child = self.hand_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for card in self.player.hand:
            btn = QPushButton(f'{card.name}\n{card.description}\n({card.card_type})\nCost: {card.cost}')
            btn.clicked.connect(lambda _, c=card: self.play_card(c))
            self.hand_layout.addWidget(btn)

        # 更新抽牌堆显示
        self.deck_list.clear()
        for card in self.player.deck:
            self.deck_list.addItem(f'{card.name}: {card.description} ({card.card_type}) (Cost: {card.cost})')

        # 更新弃牌堆显示
        self.discard_pile_list.clear()
        for card in self.player.discard_pile:
            self.discard_pile_list.addItem(f'{card.name}: {card.description} ({card.card_type}) (Cost: {card.cost})')

    def play_card(self, card):
        # 播放卡片动作
        result = card.play(self.player, self.enemy)
        self.info_label.setText(result)
        if 'Not enough energy' not in result:
            self.player.discard_pile.append(card)  # 将打出的卡牌放入弃牌堆
            self.player.hand.remove(card)
        self.update_status()
        if self.enemy.hp <= 0:
            QMessageBox.information(self, 'Victory', 'You defeated the enemy!')
            self.close()

    def update_status(self):
        # 更新状态显示
        self.energy_label.setText(f'Energy: {self.player.energy}')
        self.player_hp_label.setText(f'Player HP: {self.player.hp}/{self.player.max_hp} Armor: {self.player.armor}')
        self.enemy_hp_label.setText(f'Enemy HP: {self.enemy.hp} Armor: {self.enemy.armor}')
        self.update_hand()

    def start_player_turn(self):
        # 开始玩家回合
        self.player.energy = 3
        self.player.armor = 0  # 回合开始时护甲值降为0
        self.enemy.armor = 0  # 敌人护甲值降为0
        self.player.hand = []
        self.player.draw_cards(5)  # 每回合开始时抽取5张牌
        self.update_status()

    def end_turn(self):
        # 结束回合
        result = self.enemy.attack(self.player)
        self.info_label.setText(result)
        if self.player.hp <= 0:
            QMessageBox.information(self, 'Defeat', 'You have been defeated!')
            self.close()
        else:
            # 将所有手牌放入弃牌堆
            self.player.discard_pile.extend(self.player.hand)
            self.player.hand = []
            self.start_player_turn()

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
