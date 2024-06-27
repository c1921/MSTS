class Trait:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def apply(self, target):
        pass

class Notochord(Trait):
    def __init__(self):
        super().__init__('Notochord', 'Grants 3 layers of Nimbleness.')

    def apply(self, target):
        target.add_state('Nimbleness', 3)
        return f'{target.name} gains 3 layers of Nimbleness!'

# 将所有性状添加到列表中
all_traits = [Notochord()]
