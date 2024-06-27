from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QPushButton, QMessageBox, QProgressBar, QHBoxLayout
from card_button import CardButton
from game_logic import GameLogic
from resources.cards import all_cards
from reward_window import RewardWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.game_logic = GameLogic(self)

        self.initUI()
        self.game_logic.start_player_turn()

    def initUI(self):
        self.setWindowTitle('Minimal Slay the Spire')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        self.info_label = QLabel('Welcome to the battle!')
        main_layout.addWidget(self.info_label)

        self.layer_label = QLabel('Layer: 1')
        main_layout.addWidget(self.layer_label)

        self.traits_label = QLabel('Traits:')
        main_layout.addWidget(self.traits_label)

        player_layout = QVBoxLayout()
        self.energy_label = QLabel(f'Energy: 0/0')
        player_layout.addWidget(self.energy_label)

        self.player_hp_label = QLabel(f'Player HP: 0/0 Armor: 0')
        player_layout.addWidget(self.player_hp_label)

        self.player_hp_bar = QProgressBar()
        player_layout.addWidget(self.player_hp_bar)

        self.player_states_label = QLabel('States:')
        player_layout.addWidget(self.player_states_label)

        enemy_layout = QVBoxLayout()
        self.enemy_info_label = QLabel(f'Enemy: None\nHP: 0/0\nAttack: 0\nArmor: 0')
        enemy_layout.addWidget(self.enemy_info_label)

        self.enemy_hp_bar = QProgressBar()
        enemy_layout.addWidget(self.enemy_hp_bar)

        self.enemy_states_label = QLabel('States:')
        enemy_layout.addWidget(self.enemy_states_label)

        info_layout = QHBoxLayout()
        info_layout.addLayout(player_layout)
        info_layout.addLayout(enemy_layout)
        main_layout.addLayout(info_layout)

        self.hand_count_label = QLabel('Hand: 0')
        main_layout.addWidget(self.hand_count_label)

        self.hand_layout = QVBoxLayout()
        main_layout.addLayout(self.hand_layout)

        self.deck_layout = QVBoxLayout()
        main_layout.addLayout(self.deck_layout)
        self.deck_count_label = QLabel('Deck: 0')
        self.deck_list = QListWidget()
        self.deck_layout.addWidget(self.deck_count_label)
        self.deck_layout.addWidget(self.deck_list)

        self.discard_pile_layout = QVBoxLayout()
        main_layout.addLayout(self.discard_pile_layout)
        self.discard_pile_count_label = QLabel('Discard Pile: 0')
        self.discard_pile_list = QListWidget()
        self.discard_pile_layout.addWidget(self.discard_pile_count_label)
        self.discard_pile_layout.addWidget(self.discard_pile_list)

        self.all_cards_list = QListWidget()
        for card in all_cards:
            self.all_cards_list.addItem(f'{card.name}: {card.description} ({card.card_type}) (Cost: {card.cost})')
        main_layout.addWidget(self.all_cards_list)

        self.gold_label = QLabel('Gold: 0')
        main_layout.addWidget(self.gold_label)

        self.end_turn_button = QPushButton('End Turn')
        self.end_turn_button.clicked.connect(self.game_logic.end_turn)
        main_layout.addWidget(self.end_turn_button)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def update_hand(self, hand_cards):
        while self.hand_layout.count():
            child = self.hand_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for card in hand_cards:
            card_button = CardButton(card, self.game_logic.play_card)
            self.hand_layout.addWidget(card_button)

    def update_deck(self, deck_cards):
        self.deck_list.clear()
        for card in deck_cards:
            self.deck_list.addItem(f'{card.name}: {card.description} ({card.card_type}) (Cost: {card.cost})')

    def update_discard_pile(self, discard_pile_cards):
        self.discard_pile_list.clear()
        for card in discard_pile_cards:
            self.discard_pile_list.addItem(f'{card.name}: {card.description} ({card.card_type}) (Cost: {card.cost})')

    def update_status_labels(self, player_energy, player_max_energy, player_hp, player_max_hp, player_armor, enemy_name, enemy_hp, enemy_max_hp, enemy_attack_power, enemy_armor, gold, layer):
        self.energy_label.setText(f'Energy: {player_energy}/{player_max_energy}')
        self.player_hp_label.setText(f'Player HP: {player_hp}/{player_max_hp} Armor: {player_armor}')
        self.player_hp_bar.setMaximum(player_max_hp)
        self.player_hp_bar.setValue(player_hp)

        self.enemy_info_label.setText(f'Enemy: {enemy_name}\nHP: {enemy_hp}/{enemy_max_hp}\nAttack: {enemy_attack_power}\nArmor: {enemy_armor}')
        self.enemy_hp_bar.setMaximum(enemy_max_hp)
        self.enemy_hp_bar.setValue(enemy_hp)

        self.hand_count_label.setText(f'Hand: {len(self.game_logic.player.hand)}')
        self.deck_count_label.setText(f'Deck: {len(self.game_logic.player.deck)}')
        self.discard_pile_count_label.setText(f'Discard Pile: {len(self.game_logic.player.discard_pile)}')
        self.gold_label.setText(f'Gold: {gold}')
        self.layer_label.setText(f'Layer: {layer}')

        self.update_states()

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
        self.game_logic.update_status()

    def close_game(self, title, message):
        QMessageBox.information(self, title, message)
        self.close()
