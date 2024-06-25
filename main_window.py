from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QPushButton, QMessageBox
from card_button import CardButton
from game_logic import GameLogic
from resources.cards import all_cards

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.game_logic = GameLogic(self)

        self.initUI()
        self.game_logic.start_player_turn()

    def initUI(self):
        self.setWindowTitle('Slay the Spire Clone')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # 显示游戏信息的标签
        self.info_label = QLabel('Welcome to the battle!')
        self.layout.addWidget(self.info_label)

        # 显示玩家能量的标签
        self.energy_label = QLabel(f'Energy: 0')
        self.layout.addWidget(self.energy_label)

        # 显示玩家HP和护甲的标签
        self.player_hp_label = QLabel(f'Player HP: 0/0 Armor: 0')
        self.layout.addWidget(self.player_hp_label)

        # 显示敌人信息的标签
        self.enemy_info_label = QLabel(f'Enemy: None\nHP: 0/0\nAttack: 0\nArmor: 0')
        self.layout.addWidget(self.enemy_info_label)

        # 显示手牌数量的标签
        self.hand_count_label = QLabel('Hand: 0')
        self.layout.addWidget(self.hand_count_label)

        # 显示玩家手牌的布局
        self.hand_layout = QVBoxLayout()  # 将手牌布局改为纵向排列
        self.layout.addLayout(self.hand_layout)

        # 显示抽牌堆的布局和数量标签
        self.deck_layout = QVBoxLayout()
        self.layout.addLayout(self.deck_layout)
        self.deck_count_label = QLabel('Deck: 0')
        self.deck_list = QListWidget()
        self.deck_layout.addWidget(self.deck_count_label)
        self.deck_layout.addWidget(self.deck_list)

        # 显示弃牌堆的布局和数量标签
        self.discard_pile_layout = QVBoxLayout()
        self.layout.addLayout(self.discard_pile_layout)
        self.discard_pile_count_label = QLabel('Discard Pile: 0')
        self.discard_pile_list = QListWidget()
        self.discard_pile_layout.addWidget(self.discard_pile_count_label)
        self.discard_pile_layout.addWidget(self.discard_pile_list)

        # 显示所有卡片种类的列表
        self.all_cards_list = QListWidget()
        for card in all_cards:
            self.all_cards_list.addItem(f'{card.name}: {card.description} ({card.card_type}) (Cost: {card.cost})')
        self.layout.addWidget(self.all_cards_list)

        # 结束回合的按钮
        self.end_turn_button = QPushButton('End Turn')
        self.end_turn_button.clicked.connect(self.game_logic.end_turn)
        self.layout.addWidget(self.end_turn_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def update_hand(self, hand_cards):
        # 更新玩家手牌显示
        while self.hand_layout.count():
            child = self.hand_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for card in hand_cards:
            card_button = CardButton(card, self.game_logic.play_card)
            self.hand_layout.addWidget(card_button)

    def update_deck(self, deck_cards):
        # 更新抽牌堆显示
        self.deck_list.clear()
        for card in deck_cards:
            self.deck_list.addItem(f'{card.name}: {card.description} ({card.card_type}) (Cost: {card.cost})')

    def update_discard_pile(self, discard_pile_cards):
        # 更新弃牌堆显示
        self.discard_pile_list.clear()
        for card in discard_pile_cards:
            self.discard_pile_list.addItem(f'{card.name}: {card.description} ({card.card_type}) (Cost: {card.cost})')

    def update_status_labels(self, player_energy, player_hp, player_max_hp, player_armor, enemy_name, enemy_hp, enemy_max_hp, enemy_attack_power, enemy_armor):
        # 更新状态显示
        self.energy_label.setText(f'Energy: {player_energy}')
        self.player_hp_label.setText(f'Player HP: {player_hp}/{player_max_hp} Armor: {player_armor}')
        self.enemy_info_label.setText(f'Enemy: {enemy_name}\nHP: {enemy_hp}/{enemy_max_hp}\nAttack: {enemy_attack_power}\nArmor: {enemy_armor}')
        self.hand_count_label.setText(f'Hand: {len(self.game_logic.player.hand)}')
        self.deck_count_label.setText(f'Deck: {len(self.game_logic.player.deck)}')
        self.discard_pile_count_label.setText(f'Discard Pile: {len(self.game_logic.player.discard_pile)}')

    def close_game(self, title, message):
        QMessageBox.information(self, title, message)
        self.close()
