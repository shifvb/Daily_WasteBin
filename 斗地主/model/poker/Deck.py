import numpy as np
from model.poker.Suit import Suit, SpecialSuit
from model.poker.Rank import Rank
from model.poker.Card import PlayingCard, SpecialPlayingCard

_suits = [Suit.spade, Suit.heart, Suit.diamond, Suit.club]
_special_suits = [SpecialSuit.red_joker, SpecialSuit.black_joker]
_ranks = [Rank.ace, Rank.deuce, Rank.three, Rank.four, Rank.five, Rank.six, Rank.seven, Rank.eight, Rank.nine, Rank.ten,
          Rank.jack, Rank.queen, Rank.king]


class CardDeck(object):
    def __init__(self):
        """一副牌"""
        self.cards = list()

    def full_init(self):
        """码牌"""
        # 52张普通花色牌
        for _suit in _suits:
            for _rank in _ranks:
                self.cards.append(PlayingCard(_suit, _rank))
        # 2张大小王
        for _special_suit in _special_suits:
            self.cards.append(SpecialPlayingCard(_special_suit))

    def clear(self):
        """清除一副牌"""
        self.cards.clear()

    def shuffle_cards(self):
        """洗牌"""
        card_num = len(self.cards)
        _random_list = np.array(list(range(card_num)))
        np.random.shuffle(_random_list)
        self.cards = [self.cards[idx] for idx in _random_list]

    def __str__(self):
        return "<class CardDeck> [" + ", ".join([card.get_str_zh_cn() for card in self.cards]) + "]"

    __repr__ = __str__


if __name__ == '__main__':
    cd = CardDeck()
    cd.full_init()
    print(cd)
    cd.clear()
    print(cd)
