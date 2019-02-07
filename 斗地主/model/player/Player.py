import copy
from model.player.Role import UndefinedRole, LandlordRole, FarmerRole
from lang.zh_cn import ZH_CN


class Player(object):
    def __init__(self, name):
        self.cards = list()
        self.role = UndefinedRole()
        self.name = name

    def sort_cards(self):
        self.cards.sort(key=lambda x: x.rank * 100 + x.suit, reverse=True)

    def play_cards(self, cards):
        """出牌"""
        for card in cards:
            self.cards.remove(card)

    def __str__(self):
        _pre = "{}".format(self.name)
        if isinstance(self.role, FarmerRole):
            _pre += "[农民]"
        elif isinstance(self.role, LandlordRole):
            _pre += "[地主]"
        else:
            _pre += "[玩家]"
        _pre += "[{}张]".format(len(self.cards))

        _str = "\t\t"
        for _card in self.cards:
            if str(ZH_CN[_card.rank]) in _str:
                _str += "{}".format(ZH_CN[_card.rank])
            elif str(ZH_CN[_card.rank]) in "A23456789JQK10":
                _str += "{:>4}".format(ZH_CN[_card.rank])
            else:
                _str += "{:>2}".format(ZH_CN[_card.rank])

        return _pre + _str
