import copy
import numpy as np

from lang.zh_cn import ZH_CN
from model.poker.CardGroup import CardGroup
from model.poker.Card import Rank, Suit, Card
from model.player.Player import Player
from model.player.Role import LandlordRole, FarmerRole


class Game(object):
    def __init__(self):
        # 初始化玩家
        self.player1 = Player("Player1")
        self.player2 = Player("Player2")
        self.player3 = Player("Player3")
        self.card_list = self.init_cards()  # 初始化牌 & 洗牌
        self.send_cards()  # 发牌

        # 抢地主阶段
        self.current_player = None  # 当前要出牌的玩家指针，一定是地主出牌
        self.landlord = None  # 地主指针
        self.farmers = None  # 农民列表
        self.all_players = (self.player1, self.player2, self.player3)  # 所有玩家的列表
        self.re_rob_landlord_counter = 0  # 所有玩家都不叫地主的计数，如果超过3次就流局，游戏结束
        while not self.select_landlord_console():  # 抢地主循环
            pass

        # 出牌阶段
        self.max_group = None  # 当前最大牌
        self.max_player = None  # 最大牌对应的那个人
        self.max_counter = 0  # 出完牌以后有多少个人不要，如果到了2，就意味着一个人出牌，其他人不要了。那么这个人有牌权。
        self.winner = None  # 赢家
        while True:
            if self.is_game_ended():
                print("游戏结束！恭喜{}获胜!".format(self.winner.name))
                exit()
            self.play_card_console()  # 开始出牌

    @staticmethod
    def init_cards():
        _suits = [Suit.HEART, Suit.SPADE, Suit.CLUB, Suit.DIAMOND]
        _ranks = [Rank.ACE, Rank.DEUCE, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE,
                  Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING]
        # 生成牌
        _card_list = list()
        for _suit in _suits:
            for _rank in _ranks:
                _card_list.append(Card(_suit, _rank))
        _card_list.append(Card(Suit.OTHER, Rank.RED_JOKER))  # 大王
        _card_list.append(Card(Suit.OTHER, Rank.BLACK_JOKER))  # 小王
        # 洗牌
        _card_num = len(_card_list)
        _arr = np.array(list(range(_card_num)))
        np.random.shuffle(_arr)
        return [_card_list[idx] for idx in _arr]

    def is_game_ended(self):
        """判断游戏是否结束"""
        if len(self.player1.cards) == 0:
            self.winner = self.player1
            return True
        if len(self.player2.cards) == 0:
            self.winner = self.player2
            return True
        if len(self.player3.cards) == 0:
            self.winner = self.player3
            return True
        return False

    def send_cards(self):
        """发牌"""
        # 发牌前先清除掉原有的牌
        self.player1.cards.clear()
        self.player2.cards.clear()
        self.player3.cards.clear()
        # 发牌
        while len(self.card_list) > 3:
            _this_card = self.card_list.pop()
            self.player1.cards.append(_this_card)
            _this_card = self.card_list.pop()
            self.player2.cards.append(_this_card)
            _this_card = self.card_list.pop()
            self.player3.cards.append(_this_card)
        self.player1.sort_cards()
        self.player2.sort_cards()
        self.player3.sort_cards()
        if not len(self.card_list) == 3:
            raise ValueError("it should be 3, rather than {}".format(len(self.card_list)))

    def select_landlord_console(self):
        """抢地主console版本"""
        # 抢地主失败3次为流局
        if self.re_rob_landlord_counter == 3:
            print("流局! 游戏结束")
            exit()

        print("抢地主！！！ 手牌如下：")
        [print(_) for _ in self.all_players]

        # 所有要抢地主的人
        _active_players = list(self.all_players)
        # 以及其对应状态
        _players_status = [False for _ in range(len(_active_players))]

        # 定义一个便捷函数
        def _get_input_from_console(_name) -> bool:
            """
            获取用户要不要抢地主
            :return: True，抢地主；False，不抢地主
            """
            while True:  # 获得用户输入循环
                _s = input("{}: 您是否抢地主？[Y/N]\t".format(_name))
                if _s.upper() == "Y":
                    return True
                elif _s.upper() == "N":
                    return False
                else:
                    pass

        # 询问所有要抢地主的人，是否要抢地主？
        for idx in range(len(_active_players)):
            _players_status[idx] = _get_input_from_console(_active_players[idx].name)
        # 判断抢地主结果
        if sum(_players_status) == 0:  # 流局
            self.re_rob_landlord_counter += 1  # 抢地主失败，流局计数器加1
            self.card_list = self.init_cards()  # 初始化牌 & 洗牌
            self.send_cards()  # 发牌
            return False
        elif sum(_players_status) == 1:  # 只有1人抢地主，那么地主就是这个抢地主的玩家
            _landlord = _active_players[_players_status.index(True)]
        else:  # 多人要地主，再次询问一下最早抢地主的人要不要
            _active_players = filter(lambda x: x[0], zip(_players_status, _active_players))  # 滤掉不要地主的玩家
            _active_players = list(map(lambda x: x[1], _active_players))
            if _get_input_from_console(_active_players[0].name) is True:  # 这个人要了，它是地主
                _landlord = _active_players[0]
            else:  # 这个人不要，下家是地主
                _landlord = _active_players[1]

        _farmers = [_ for _ in list(self.all_players) if _ is not _landlord]  # 不是地主的玩家为农民

        print("地主抢牌：", end=" ")
        [print("{}".format(ZH_CN[_.rank]), end=" ") for _ in self.card_list]
        print("\n")
        self._select_landlord(_landlord, _farmers)
        return True

    def _next_player(self):
        """
        返回self.current_player的下一个玩家
        :return: 下一个玩家指针
        """
        _idx = self.all_players.index(self.current_player)
        return self.all_players[0] if _idx == 2 else self.all_players[_idx + 1]

    def _select_landlord(self, landlord: Player, farmers: list):
        """用于选定地主"""
        # 设定地主和农民
        landlord.role = LandlordRole()
        self.landlord = landlord
        farmers[0].role = FarmerRole()
        farmers[1].role = FarmerRole()
        self.farmers = farmers

        # 给地主发牌
        for _ in range(len(self.card_list)):
            self.landlord.cards.append(self.card_list.pop())
        self.landlord.sort_cards()

        # 从地主开始出牌
        self.current_player = self.landlord

    def is_success(self):
        """判断是不是有人已经出完了"""
        return len(self.player1.cards) == 0 or len(self.player2.cards) == 0 or len(self.player3.cards) == 0

    def parse_cards_console(self):
        """
        获取出牌命令行版本
        :return: card_out 出牌列表，或者是 False（要不起）
        """

        def _is_in_player(_input_ranks_str, _player):
            """
            判断用户从命令行输入的是不是玩家手牌里（不能出没有的牌）
            :param _input_ranks_str: 命令行输入的牌的大小，字符串
            :param _player: 玩家
            :return: 命令行输入的牌（如果有的话）
                    False （如果没有的话）
            """
            _input_ranks = list()
            for _c in _input_ranks_str:  # 判断每个字符
                if _c == "3":
                    _input_ranks.append(Rank.THREE)
                elif _c == "4":
                    _input_ranks.append(Rank.FOUR)
                elif _c == "5":
                    _input_ranks.append(Rank.FIVE)
                elif _c == "6":
                    _input_ranks.append(Rank.SIX)
                elif _c == "7":
                    _input_ranks.append(Rank.SEVEN)
                elif _c == "8":
                    _input_ranks.append(Rank.EIGHT)
                elif _c == "9":
                    _input_ranks.append(Rank.NINE)
                elif _c == "0":
                    _input_ranks.append(Rank.TEN)
                elif _c == "J" or _c == "j":
                    _input_ranks.append(Rank.JACK)
                elif _c == "Q" or _c == "q":
                    _input_ranks.append(Rank.QUEEN)
                elif _c == "K" or _c == "k":
                    _input_ranks.append(Rank.KING)
                elif _c == "A" or _c == "a":
                    _input_ranks.append(Rank.ACE)
                elif _c == "2":
                    _input_ranks.append(Rank.DEUCE)
                elif _c == "X" or _c == "x":
                    _input_ranks.append(Rank.BLACK_JOKER)
                elif _c == "D" or _c == 'd':
                    _input_ranks.append(Rank.RED_JOKER)
                else:
                    return False  # 如果是非法字符，直接就False了
            _this_cards = copy.deepcopy(_player.cards)
            _cards_out = list()
            for _input_rank in _input_ranks:
                _in_flag = False
                _idx_memory = None
                for _idx, _this_card in enumerate(_this_cards):
                    if _input_rank == _this_card.rank:
                        _in_flag = True
                        _idx_memory = _idx
                        break
                if _in_flag is True:  # 找到了,加到临时列表中
                    _cards_out.append(_this_cards.pop(_idx_memory))
                else:
                    return False  # 只要输入的牌有一张找不到，就不行
            return _cards_out  # 返回输出的牌

        while True:
            # 展示出牌界面
            self.print_status_console()
            s = input("[{}] 出牌 (34567890JQKA2XD), 要不起（N）:\t".format(self.current_player.name))  # 获取用户输入
            if s == "N" or s == "n":  # 要不起
                if self.max_player is None:
                    print("必须出牌！")
                    continue  # 如果无效，就再来一次
                else:
                    return None  # 别人出的管不上，那么返回None
            if len(s) == 0:  # 空字符串肯定无效
                print("无效出牌！")
                continue  # 如果无效，就再来一次
            input_cards = _is_in_player(s, self.current_player)
            if input_cards is False:  # 不在玩家手牌里，无效
                print("不能出没有的牌")
                continue  # 如果无效，就再来一次
            if CardGroup(input_cards).is_valid() is False:  # 不符合出牌规则，无效
                print("不符合出牌规则")
                continue  # 如果无效，就再来一次
            if self.max_group is not None and not CardGroup(input_cards).is_greater(self.max_group):  # 比人牌小，无效
                print("emmmm，比人家牌小")
                continue  # 如果无效，就再来一次
            # 如果经过上述的测试，是有效的，那么就返回parse到的牌
            return input_cards

    def play_card_console(self):
        # 都要不起,重置状态和计数器
        if self.max_counter == 2:
            self.max_counter = 0
            self.max_group = None
            self.max_player = None

        # 获取self.current_player玩家的出牌
        input_cards = self.parse_cards_console()
        self.print_cards_console(self.current_player.name, input_cards)

        # 要不起，直接下一位
        if input_cards is None:
            self.current_player = self._next_player()
            self.max_counter += 1
            return

        # 要得起，出牌
        self.max_group = CardGroup(input_cards)  # 赋值
        self.max_player = self.current_player  # 赋值
        self.max_counter = 0  # 赋值
        self.current_player.play_cards(input_cards)  # 出牌
        self.current_player = self._next_player()  # 出完牌了，轮到下一位
        # self.print_status_console()

    def print_status_console(self):
        for x in (self.player1, self.player2, self.player3):
            if self.current_player is not None and x is self.current_player:
                print("-> ", end="")
            print(x)

    @staticmethod
    def print_cards_console(player_name, cards):
        if cards is None:  # 要不起
            print("[{}] 要不起".format(player_name))
            return
        print("[{}] 出了 ".format(player_name), end="")
        for x in cards:
            print("{}".format(ZH_CN[x.rank]), end="")
        print("\t\t(", end="")
        for x in cards:
            print("{}{}".format(ZH_CN[x.suit], ZH_CN[x.rank]), end=",")
        print(")")
        print()


def main():
    Game()


if __name__ == '__main__':
    main()
