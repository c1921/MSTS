from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox, QProgressBar, QHBoxLayout, QApplication
from card_button import CardButton
from game_logic import GameLogic
from resources.cards import all_cards
from reward_window import RewardWindow
from deck_window import DeckWindow
from discard_pile_window import DiscardPileWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.game_logic = GameLogic(self)

        self.deck_window = DeckWindow(self.game_logic.player.deck)
        self.discard_pile_window = DiscardPileWindow(self.game_logic.player.discard_pile)

        self.initUI()
        self.load_stylesheet()
        self.game_logic.start_player_turn()

    def initUI(self):
        self.setWindowTitle('Minimal Slay the Spire')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QHBoxLayout()  # 修改为水平布局

        left_layout = QVBoxLayout()  # 左侧布局

        self.info_label = QLabel('Welcome to the battle!')
        left_layout.addWidget(self.info_label)

        self.layer_label = QLabel('Layer: 1')
        left_layout.addWidget(self.layer_label)

        self.traits_label = QLabel('Traits:')
        left_layout.addWidget(self.traits_label)

        self.hand_count_label = QLabel('Hand: 0')
        left_layout.addWidget(self.hand_count_label)

        self.hand_layout = QVBoxLayout()
        left_layout.addLayout(self.hand_layout)

        deck_button = QPushButton('Open Deck')
        deck_button.clicked.connect(self.open_deck_window)
        left_layout.addWidget(deck_button)

        discard_pile_button = QPushButton('Open Discard Pile')
        discard_pile_button.clicked.connect(self.open_discard_pile_window)
        left_layout.addWidget(discard_pile_button)

        self.gold_label = QLabel('Gold: 0')
        left_layout.addWidget(self.gold_label)

        self.end_turn_button = QPushButton('End Turn')
        self.end_turn_button.clicked.connect(self.game_logic.end_turn)
        left_layout.addWidget(self.end_turn_button)

        right_layout = QVBoxLayout()  # 右侧布局

        enemy_layout = QVBoxLayout()
        self.enemy_info_label = QLabel(f'Enemy: None\nHP: 0/0\nAttack: 0\nArmor: 0')
        enemy_layout.addWidget(self.enemy_info_label)

        self.enemy_hp_bar = QProgressBar()
        enemy_layout.addWidget(self.enemy_hp_bar)

        self.enemy_states_label = QLabel('States:')
        enemy_layout.addWidget(self.enemy_states_label)

        player_layout = QVBoxLayout()
        self.energy_label = QLabel(f'Energy: 0/0')
        player_layout.addWidget(self.energy_label)

        self.player_hp_label = QLabel(f'Player HP: 0/0 Armor: 0')
        player_layout.addWidget(self.player_hp_label)

        self.player_hp_bar = QProgressBar()
        player_layout.addWidget(self.player_hp_bar)

        self.player_states_label = QLabel('States:')
        player_layout.addWidget(self.player_states_label)

        right_layout.addLayout(enemy_layout)  # 敌人信息在上
        right_layout.addLayout(player_layout)  # 玩家信息在下

        main_layout.addLayout(left_layout)  # 左侧布局添加到主布局
        main_layout.addLayout(right_layout)  # 右侧布局添加到主布局

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_stylesheet(self):
        with open('dark_theme.qss', 'r') as file:
            self.setStyleSheet(file.read())

    def update_hand(self, hand_cards):
        while self.hand_layout.count():
            child = self.hand_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for card in hand_cards:
            card_button = CardButton(card, self.game_logic.play_card)
            self.hand_layout.addWidget(card_button)

    def open_deck_window(self):
        self.deck_window.show()

    def open_discard_pile_window(self):
        self.discard_pile_window.show()

    def update_status_labels(self, player_energy, player_max_energy, player_hp, player_max_hp, player_armor, enemy_name, enemy_hp, enemy_max_hp, enemy_attack_power, enemy_armor, gold, layer):
        self.energy_label.setText(f'Energy: {player_energy}/{player_max_energy}')
        self.player_hp_label.setText(f'Player HP: {player_hp}/{player_max_hp} Armor: {player_armor}')
        self.player_hp_bar.setMaximum(player_max_hp)
        self.player_hp_bar.setValue(player_hp)

        self.enemy_info_label.setText(f'Enemy: {enemy_name}\nHP: {enemy_hp}/{enemy_max_hp}\nAttack: {enemy_attack_power}\nArmor: {enemy_armor}')
        self.enemy_hp_bar.setMaximum(enemy_max_hp)
        self.enemy_hp_bar.setValue(enemy_hp)

        self.hand_count_label.setText(f'Hand: {len(self.game_logic.player.hand)}')
        self.gold_label.setText(f'Gold: {gold}')
        self.layer_label.setText(f'Layer: {layer}')

        self.update_states()

        # 更新窗口内容
        self.deck_window.update_deck_list(self.game_logic.player.deck)
        self.discard_pile_window.update_discard_pile_list(self.game_logic.player.discard_pile)

    def update_states(self):
        # 更新玩家状态显示
        player_states = ', '.join([f'{state}*{amount}' for state, amount in self.game_logic.player.states.items()])
        self.player_states_label.setText(f'States: {player_states}')

        # 更新敌人状态显示
        enemy_states = ', '.join([f'{state}*{amount}' for state, amount in self.game_logic.enemy.states.items()])
        self.enemy_states_label.setText(f'States: {enemy_states}')

    def update_traits(self, traits):
        # 更新性状显示
        trait_descriptions = ', '.join([f'{trait.name}: {trait.description}' for trait in traits])
        self.traits_label.setText(f'Traits: {trait_descriptions}')

    def show_reward_window(self, reward_cards):
        reward_window = RewardWindow(reward_cards, self.add_card_to_deck)
        reward_window.exec()

    def add_card_to_deck(self, card):
        self.game_logic.player.deck.append(card)
        self.game_logic.reset_deck()
        self.game_logic.update_status()

    def close_game(self, title, message):
        QMessageBox.information(self, title, message)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
