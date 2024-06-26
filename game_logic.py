from player import Player
from enemy import Enemy, Goblin, Orc, Dragon
from resources.cards import all_cards, Strike, Defend, Fireball, ComboStrike
import random

class GameLogic:
    def __init__(self, ui):
        self.ui = ui
        self.layer = 1
        self.player = Player('Hero', 30, 3)
        self.enemy = Goblin()
        self.gold = 0

        # 初始化玩家的卡组
        self.player.deck = [Strike()]*5 + [Defend()]*5 + [Fireball()] + [ComboStrike()]*3
        random.shuffle(self.player.deck)

    def update_status(self):
        # 更新状态显示
        self.ui.update_status_labels(
            player_energy=self.player.energy,
            player_hp=self.player.hp,
            player_max_hp=self.player.max_hp,
            player_armor=self.player.armor,
            enemy_name=self.enemy.name,
            enemy_hp=self.enemy.hp,
            enemy_max_hp=self.enemy.max_hp,
            enemy_attack_power=self.enemy.attack_power,
            enemy_armor=self.enemy.armor,
            gold=self.gold
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
            self.gold += 50
            self.show_reward_window()
            if self.layer == 1:
                self.layer += 1
                self.enemy = Orc()
                self.ui.info_label.setText('You defeated the Goblin! A new enemy approaches: Orc')
                self.start_player_turn()
            elif self.layer == 2:
                self.layer += 1
                self.enemy = Dragon()
                self.ui.info_label.setText('You defeated the Orc! A new enemy approaches: Dragon')
                self.start_player_turn()
            else:
                self.ui.close_game('Victory', 'You defeated the Dragon and won the game!')

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

    def show_reward_window(self):
        # 显示奖励窗口
        reward_cards = random.sample(all_cards, 3)
        self.ui.show_reward_window(reward_cards)
