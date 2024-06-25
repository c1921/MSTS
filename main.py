import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox, QListWidget, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

from resources.cards import all_cards, strike, defend, fireball, combo_strike
from player import Player
from enemy import Enemy

class CardButton(QFrame):
    def __init__(self, card, play_card_callback):
        super().__init__()
        self.card = card
        self.play_card_callback = play_card_callback

        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(2)

        layout = QVBoxLayout()

        h_layout = QHBoxLayout()

        self.card_name = QLabel(f'{self.card.name}')
        self.card_cost = QLabel(f'Cost: {self.card.cost}')
        self.card_description = QLabel(f'{self.card.description}\n({self.card.card_type})')

        h_layout.addWidget(self.card_name)
        h_layout.addStretch()
        h_layout.addWidget(self.card_cost)

        layout.addLayout(h_layout)
        layout.addWidget(self.card_description)

        self.setLayout(layout)

    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("background-color: lightgray;")

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.setStyleSheet("background-color: white;")

    def mousePressEvent(self, event):
        self.play_card_callback(self.card)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.player = Player('Hero', 30, 3)
        self.enemy = Enemy('Slime', 20, 5)

        # 初始化玩家的卡组
        self.player.deck = [strike]*5 + [defend]*5 + [fireball] + [combo_strike]*3
        random.shuffle(self.player.deck)

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
        self.hand_layout = QVBoxLayout()  # 将手牌布局改为纵向排列
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
            card_button = CardButton(card, self.play_card)
            self.hand_layout.addWidget(card_button)

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
        result = card.play(self.player, self.enemy, self.player.last_played_card)
        self.info_label.setText(result)
        if 'Not enough energy' not in result:
            self.player.discard_pile.append(card)  # 将打出的卡牌放入弃牌堆
            self.player.hand.remove(card)
            self.player.last_played_card = card  # 更新最后打出的卡牌
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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 加载样式表
    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
