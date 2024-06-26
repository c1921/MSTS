import math

class State:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def apply(self, target):
        pass

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

# 将所有状态效果添加到列表中
all_states = [Poison()]
