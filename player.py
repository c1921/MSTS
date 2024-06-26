import random

class Player:
    def __init__(self, name, max_hp, max_energy):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_energy = max_energy
        self.energy = max_energy
        self.armor = 0
        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.last_played_card = None
        self.states = {}  # 状态属性

    def draw_cards(self, num_cards):
        for _ in range(num_cards):
            if not self.deck:
                self.deck, self.discard_pile = self.discard_pile, self.deck
                random.shuffle(self.deck)
            if self.deck:
                self.hand.append(self.deck.pop())

    def restore_energy(self):
        self.energy = self.max_energy

    def add_state(self, state_name, amount):
        if state_name in self.states:
            self.states[state_name] += amount
        else:
            self.states[state_name] = amount

    def remove_state(self, state_name, amount):
        if state_name in self.states:
            self.states[state_name] -= amount
            if self.states[state_name] <= 0:
                del self.states[state_name]
