# 扑克牌大小实际值
THREE = 3
FOUR = 4
FIVE = 5
SIX = 6
SEVEN = 7
EIGHT = 8
NINE = 9
TEN = 10
JACK = 11
QUEEN = 12
KING = 13
ACE = 14
DEUCE = 15
BLACK_JOKER = 16
RED_JOKER = 17

# 扑克牌花色实际值
CLUB = 21
DIAMOND = 22
SPADE = 23
HEART = 24
OTHER = 25


class Rank(object):  # 扑克牌的大小
    ACE = ACE
    DEUCE = DEUCE
    THREE = THREE
    FOUR = FOUR
    FIVE = FIVE
    SIX = SIX
    SEVEN = SEVEN
    EIGHT = EIGHT
    NINE = NINE
    TEN = TEN
    JACK = JACK
    QUEEN = QUEEN
    KING = KING
    BLACK_JOKER = BLACK_JOKER
    RED_JOKER = RED_JOKER


class Suit(object):  # 扑克牌花色
    SPADE = SPADE  # 黑桃♠
    HEART = HEART  # 红桃♥
    DIAMOND = DIAMOND  # 方块♦
    CLUB = CLUB  # 梅花♣
    OTHER = OTHER


class Card(object):
    def __init__(self, suit, rank):
        """扑克牌类"""
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank


def test():
    r = Rank
    assert r.RED_JOKER > r.BLACK_JOKER
    assert r.BLACK_JOKER > r.DEUCE
    assert r.JACK > r.THREE
    assert r.JACK > r.TEN
    assert r.ACE > r.KING
    assert r.THREE < r.DEUCE

    s = Suit
    assert s.OTHER > s.CLUB
    assert s.DIAMOND > s.CLUB
    assert s.HEART > s.SPADE
    assert s.SPADE > s.DIAMOND


if __name__ == '__main__':
    test()
