from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QListWidget, QWidget

class DiscardPileWindow(QMainWindow):
    def __init__(self, discard_pile):
        super().__init__()
        self.discard_pile = discard_pile
        self.initUI()
        self.load_stylesheet()

    def initUI(self):
        self.setWindowTitle('Discard Pile')
        self.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()

        self.discard_pile_list = QListWidget()
        layout.addWidget(self.discard_pile_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_discard_pile_list(self, discard_pile):
        self.discard_pile = discard_pile
        self.discard_pile_list.clear()
        for card in self.discard_pile:
            self.discard_pile_list.addItem(f'{card.name}: {card.description} ({card.card_type}) (Cost: {card.cost})')

    def load_stylesheet(self):
        with open('dark_theme.qss', 'r') as file:
            self.setStyleSheet(file.read())
