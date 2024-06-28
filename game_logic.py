from player import Player
from enemy import Enemy, Goblin, Orc, Dragon
from resources.cards import all_cards, Strike, Defend, Fireball, ComboStrike
from states import Poison, Nimbleness
from traits import Notochord
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

        # 初始化玩家的性状
        self.player.add_trait(Notochord())

    def update_status(self):
        # 更新状态显示
        self.ui.update_status_labels(
            player_energy=self.player.energy,
            player_max_energy=self.player.max_energy,
            player_hp=self.player.hp,
            player_max_hp=self.player.max_hp,
            player_armor=self.player.armor,
            enemy_name=self.enemy.name,
            enemy_hp=self.enemy.hp,
            enemy_max_hp=self.enemy.max_hp,
            enemy_attack_power=self.enemy.attack_power,
            enemy_armor=self.enemy.armor,
            gold=self.gold,
            layer=self.layer
        )
        self.ui.update_hand(self.player.hand)
        self.ui.update_traits(self.player.traits)
        self.ui.update_states()

        # 更新窗口内容
        self.ui.deck_window.update_deck_list(self.player.deck)
        self.ui.discard_pile_window.update_discard_pile_list(self.player.discard_pile)

    def apply_states(self, target):
        state_messages = []
        for state in target.states.keys():
            if state == 'Poison':
                poison = Poison()
                state_messages.append(poison.apply(target))
        return state_messages

    def modify_armor_gain(self, amount, target):
        for state in target.states.keys():
            if state == 'Nimbleness':
                nimbleness = Nimbleness()
                amount = nimbleness.modify_armor(amount, target)
        return amount

    def play_card(self, card):
        # 播放卡片动作
        if isinstance(card, Defend):
            # 计算护甲值
            armor_gain = self.modify_armor_gain(card.base_armor_gain, self.player)
            card.armor_gain = armor_gain

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
            self.reset_deck()
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
        self.player.restore_energy()
        self.player.armor = 0  # 回合开始时护甲值降为0
        self.enemy.armor = 0  # 敌人护甲值降为0
        self.player.hand = []
        self.player.draw_cards(5)  # 每回合开始时抽取5张牌
        self.update_status()

    def end_turn(self):
        # 结束回合
        result = self.enemy.attack(self.player)
        self.ui.info_label.setText(result)

        # 应用中毒状态效果
        player_state_messages = self.apply_states(self.player)
        enemy_state_messages = self.apply_states(self.enemy)

        # 更新状态信息
        if player_state_messages or enemy_state_messages:
            self.ui.info_label.setText('\n'.join(player_state_messages + enemy_state_messages))

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

    def reset_deck(self):
        # 将手牌、弃牌堆、摸牌堆都放回牌组并洗牌
        self.player.deck.extend(self.player.hand)
        self.player.deck.extend(self.player.discard_pile)
        self.player.hand = []
        self.player.discard_pile = []
        random.shuffle(self.player.deck)
