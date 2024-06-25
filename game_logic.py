from player import Player
from enemy import Enemy
from resources.cards import strike, defend, fireball, combo_strike
import random

class GameLogic:
    def __init__(self, ui):
        self.ui = ui
        self.player = Player('Hero', 30, 3)
        self.enemy = Enemy('Slime', 20, 5)

        # 初始化玩家的卡组
        self.player.deck = [strike]*5 + [defend]*5 + [fireball] + [combo_strike]*3
        random.shuffle(self.player.deck)

    def update_status(self):
        # 更新状态显示
        self.ui.update_status_labels(
            player_energy=self.player.energy,
            player_hp=self.player.hp,
            player_max_hp=self.player.max_hp,
            player_armor=self.player.armor,
            enemy_hp=self.enemy.hp,
            enemy_armor=self.enemy.armor
        )
        self.ui.update_hand(self.player.hand)
        self.ui.update_deck(self.player.deck)
        self.ui.update_discard_pile(self.player.discard_pile)

    def play_card(self, card):
        # 播放卡片动作
        result = card.play(self.player, self.enemy, self.player.last_played_card)
        self.ui.info_label.setText(result)
        if 'Not enough energy' not in result:
            self.player.discard_pile.append(card)  # 将打出的卡牌放入弃牌堆
            self.player.hand.remove(card)
            self.player.last_played_card = card  # 更新最后打出的卡牌
        self.update_status()
        if self.enemy.hp <= 0:
            self.ui.close_game('Victory', 'You defeated the enemy!')

    def start_player_turn(self):
        # 开始玩家回合
        self.player.energy = 3
        self.player.armor = 0  # 回合开始时护甲值降为0
        self.enemy.armor = 0  # 敌人护甲值降为0
        self.player.hand = []
        self.player.draw_cards(5)  # 每回合开始时抽取5张牌
        self.update_status()

    def end_turn(self):
        # 结束回合
        result = self.enemy.attack(self.player)
        self.ui.info_label.setText(result)
        if self.player.hp <= 0:
            self.ui.close_game('Defeat', 'You have been defeated!')
        else:
            # 将所有手牌放入弃牌堆
            self.player.discard_pile.extend(self.player.hand)
            self.player.hand = []
            self.start_player_turn()
