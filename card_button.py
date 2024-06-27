from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class CardButton(QFrame):
    def __init__(self, card, play_card_callback):
        super().__init__()
        self.card = card
        self.play_card_callback = play_card_callback

        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(2)

        layout = QVBoxLayout()

        h_layout = QHBoxLayout()

        self.card_cost = QLabel(f'Cost: {self.card.cost}')
        self.card_name = QLabel(f'{self.card.name}')
        self.card_type = QLabel(f'{self.card.card_type}')

        self.card_cost.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.card_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_type.setAlignment(Qt.AlignmentFlag.AlignRight)

        h_layout.addWidget(self.card_cost)
        h_layout.addStretch()
        h_layout.addWidget(self.card_name)
        h_layout.addStretch()
        h_layout.addWidget(self.card_type)

        self.card_description = QLabel(f'{self.card.description}')

        layout.addLayout(h_layout)
        layout.addWidget(self.card_description)

        self.setLayout(layout)

        # 设置默认样式
        self.setStyleSheet("""
            CardButton {
                background-color: #4a4a4a;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                
            }
            QLabel {
                border: none;
                color: #ffffff;
            }
        """)

    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            CardButton {
                background-color: #5a5a5a;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                
            }
            QLabel {
                border: none;
                color: #ffffff;
            }
        """)

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.setStyleSheet("""
            CardButton {
                background-color: #4a4a4a;
                color: #ffffff;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                
            }
            QLabel {
                border: none;
                color: #ffffff;
            }
        """)

    def mousePressEvent(self, event):
        self.play_card_callback(self.card)
