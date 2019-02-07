from model.poker.Card import Card, Suit, Rank


class CardGroup(object):
    def __init__(self, cards: list):
        """卡的组合"""
        self.cards = cards  # 保存变量
        self._init_guard()  # 检查类型和数量
        self.cards.sort(key=lambda x: x.rank * 100 + x.suit, reverse=True)  # 排好序
        self._card_count, self._reverse_card_count = self._count_cards()  # 记录每种牌的数量

    def _init_guard(self):
        """看看是不是想要的类型"""
        # type check
        if not isinstance(self.cards, list):
            raise TypeError("unknown type: {}, expected 'tuple'.".format(type(self.cards)))
        for card in self.cards:
            if not isinstance(card, Card):
                raise TypeError("unknown type: {}, expected 'Card'.".format(type(card)))
        # amount check
        if len(self.cards) == 0:
            raise ValueError("card length must be greater than 0, got {}".format(len(self.cards)))

    def _count_cards(self):
        """
        内部方法，对牌进行计数，返回两个计数字典
        :return:
            card_num: 每种牌有几个，例如{J: 3个，Q：3个， K：2个}
            reverse_card_num: 有一定数量的牌都是哪种，例如{3个：[J，Q]，2个：[K]}
        """
        card_num = dict()
        reverse_card_num = dict()
        for card in self.cards:
            if card.rank not in card_num:
                card_num[card.rank] = 0
            card_num[card.rank] += 1
        for k, v in card_num.items():
            if v not in reverse_card_num:
                reverse_card_num[v] = []
            reverse_card_num[v].append(k)
        return card_num, reverse_card_num

    def is_two_jokers(self):
        """判断是否为王炸"""
        return self._card_count.keys() == {Rank.RED_JOKER, Rank.BLACK_JOKER}  # 必须只有大王和小王

    def is_repeated_cards(self):
        """
        判断重复牌组函数
        :return: (重复度，牌值)
            任意不是重复的牌,比如 333Q -> (0, None)
            2 -> (1, 2)
            33 -> (2, 3)
            77 -> (2, 7)
            666 -> (3, 6)
            KKKK -> (4, K)
            other cards -> (False, False)
        """
        if not len(self._card_count.keys()) == 1:
            return False, False
        repeat_rank = tuple(self._card_count.values())[0]
        repeat_value = tuple(self._card_count.keys())[0]
        return repeat_rank, repeat_value

    def is_cascaded_cards(self):
        """
        判断连续牌组函数
        :return: (重复度，跨度，开始)
            34567 -> (1, 5, 3)
            JJQQKKAA -> (2, 4, J)
            555 666 -> (3, 2, 5)
            other cards -> (False, False, False)
        """
        # 每种Rank的牌数量相同
        if self._reverse_card_count.keys() == {1} and len(self.cards) >= 5:  # 顺子至少5张
            repeat_rank = 1
        elif self._reverse_card_count.keys() == {2} and len(self.cards) >= 6:  # 连对至少6张
            repeat_rank = 2
        elif self._reverse_card_count.keys() == {3} and len(self.cards) >= 6:  # 飞机至少6张
            repeat_rank = 3
        else:
            return False, False, False

        # 牌组必须连续
        card_ranks = list(self._card_count.keys())
        card_ranks.sort(reverse=True)
        for i in range(len(card_ranks) - 1):
            if not card_ranks[i] - card_ranks[i + 1] == 1:
                return False, False, False

        # 不能是2，小王，大王
        for x in (Rank.DEUCE, Rank.BLACK_JOKER, Rank.RED_JOKER):
            if x in self._card_count:
                return False, False, False

        # 满足要求，返回
        return repeat_rank, card_ranks[0] - card_ranks[-1] + 1, card_ranks[-1]

    def is_attached_cards(self):
        """
        判断“带牌”牌组函数
        :return: (主部分牌数，副部分牌数，主部分大小)
            88833 -> (3, 2, 8)
            JJJ4 -> (3, 1, J)
            77788856 -> (6, 2, 7)
            555587 -> (4, 2, 5)
            other cards -> (False, False, False)
        """
        # 4带2
        if self._reverse_card_count.keys() == {1, 4} and \
                len(self._reverse_card_count[4]) == 1 and len(self._reverse_card_count[1]) == 2:
            return 4, 2, self._reverse_card_count[4][0]
        # 3带1 及其倍数
        if self._reverse_card_count.keys() == {1, 3} and \
                len(self._reverse_card_count[1]) == len(self._reverse_card_count[3]):
            _mul = len(self._reverse_card_count[3])  # 3张牌的主干部分重复的倍数，666就是一倍，而JJJQQQ就是两倍
            _tmp = self._reverse_card_count[3].copy()
            _tmp.sort(reverse=True)
            for i in range(len(_tmp) - 1):
                if not _tmp[i] - _tmp[i + 1] == 1:  # 必须是连续的
                    return False, False, False
            return 3 * _mul, 1 * _mul, _tmp[0]
        # 3带2 (3带1对) 及其倍数
        if self._reverse_card_count.keys() == {2, 3} and \
                len(self._reverse_card_count[3]) == len(self._reverse_card_count[2]):
            _mul = len(self._reverse_card_count[3])  # 3张牌的主干部分重复的倍数，666就是一倍，而JJJQQQ就是两倍
            _tmp = self._reverse_card_count[3].copy()
            _tmp.sort(reverse=True)
            for i in range(len(_tmp) - 1):
                if not _tmp[i] - _tmp[i + 1] == 1:  # 必须是连续的
                    return False, False, False
            return 3 * _mul, 2 * _mul, _tmp[0]
        return False, False, False

    def is_valid(self):
        """
        判断自身牌组是不是有效的出牌方式
        :return: bool值, 有效为True， 无效为False
        """
        if self.is_two_jokers() is not False:
            return True
        if self.is_repeated_cards()[0] is not False:
            return True
        if self.is_cascaded_cards()[0] is not False:
            return True
        if self.is_attached_cards()[0] is not False:
            return True
        return False

    def is_greater(self, other):
        """
        判断我的牌比传入的牌大
        :param other: 传入的牌组
        :return:
        """
        # 王炸最大
        if self.is_two_jokers():
            return True

        # 然后是4张相同牌组成的炸
        _rep = self.is_repeated_cards()
        _rep_other = other.is_repeated_cards()
        if _rep[0] == 4 and _rep_other[0] <= 3:  # self是炸, other不是炸
            return True
        elif _rep[0] <= 3 and _rep_other[0] == 4:  # self不是炸, other是炸
            return False
        elif _rep[0] == 4 and _rep_other[0] == 4:  # self是炸, other也是炸
            return _rep[1] > _rep_other[1]
        else:  # self不是炸, other也不是炸
            pass

        # 如果都是相同牌（非炸）,比如555,AA,QQQ,K之类的
        if _rep[0] is not False and _rep_other[0] is not False:
            if _rep[0] == _rep_other[0]:  # 相同重复类型
                return _rep[1] > _rep_other[1]
            else:  # 不同重复类型
                return False

        # 如果都是层叠牌，比如JJJQQQ,334455,45678之类的
        _cas = self.is_cascaded_cards()
        _cas_other = other.is_cascaded_cards()
        if _cas[0] is not False and _cas_other[0] is not False:
            if _cas[0:2] == _cas_other[0:2]:  # 相同层叠类型
                return _cas[2] > _cas_other[2]
            else:  # 不同层叠类型
                return False

        # 如果都是带牌，比如3334， JJJ88，4445558K之类的
        _att = self.is_attached_cards()
        _att_other = other.is_attached_cards()
        if _att[0] is not False and _att_other[0] is not False:
            if _att[0:2] == _att_other[0:2]:  # 相同带牌类型
                return _att[2] > _att_other[2]
            else:
                return False  # 不同带牌类型

        return False
