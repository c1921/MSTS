from card import Card
import random

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
        self.last_played_card = None

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
