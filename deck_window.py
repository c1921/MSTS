from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QListWidget, QWidget

class DeckWindow(QMainWindow):
    def __init__(self, deck):
        super().__init__()
        self.deck = deck
        self.initUI()
        self.load_stylesheet()

    def initUI(self):
        self.setWindowTitle('Deck')
        self.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()

        self.deck_list = QListWidget()
        layout.addWidget(self.deck_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_deck_list(self, deck):
        self.deck = deck
        self.deck_list.clear()
        for card in self.deck:
            self.deck_list.addItem(f'{card.name}: {card.description} ({card.card_type}) (Cost: {card.cost})')

    def load_stylesheet(self):
        with open('dark_theme.qss', 'r') as file:
            self.setStyleSheet(file.read())
