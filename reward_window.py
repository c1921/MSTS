from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from card_button import CardButton

class RewardWindow(QDialog):
    def __init__(self, reward_cards, add_card_callback):
        super().__init__()
        self.setWindowTitle('Choose a Reward')
        self.setGeometry(300, 300, 400, 300)
        self.add_card_callback = add_card_callback

        layout = QVBoxLayout()
        info_label = QLabel('You received 50 gold. Choose a card to add to your deck:')
        layout.addWidget(info_label)

        card_layout = QHBoxLayout()
        for card in reward_cards:
            card_button = CardButton(card, self.select_card)
            card_layout.addWidget(card_button)
        layout.addLayout(card_layout)

        skip_button = QPushButton('Skip')
        skip_button.clicked.connect(self.close)
        layout.addWidget(skip_button)

        self.setLayout(layout)
        self.load_stylesheet()

    def select_card(self, card):
        self.add_card_callback(card)
        self.accept()  # This will close the dialog

    def load_stylesheet(self):
        with open('dark_theme.qss', 'r') as file:
            self.setStyleSheet(file.read())
