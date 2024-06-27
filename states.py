import math

class State:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def apply(self, target):
        pass

    def modify_armor(self, amount, target):
        return amount

class Poison(State):
    def __init__(self):
        super().__init__('Poison', 'Deals damage at the end of each turn.')

    def apply(self, target):
        if 'Poison' in target.states:
            poison_amount = target.states['Poison']
            target.hp -= poison_amount
            target.states['Poison'] = math.ceil(poison_amount / 2)
            if target.states['Poison'] == 0:
                del target.states['Poison']
            return f'{target.name} takes {poison_amount} poison damage!'
        return f'{target.name} is not poisoned.'

class Nimbleness(State):
    def __init__(self):
        super().__init__('Nimbleness', 'Increases armor gain by the value of Nimbleness.')

    def modify_armor(self, amount, target):
        if 'Nimbleness' in target.states:
            nimbleness_amount = target.states['Nimbleness']
            return amount + nimbleness_amount
        return amount

# 将所有状态效果添加到列表中
all_states = [Poison(), Nimbleness()]
