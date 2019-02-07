from model.poker.Card import Card, Suit, Rank
from model.poker.CardGroup import CardGroup


def test():
    test_empty_cardgroup()  # 空卡组赋值测试
    test_two_jokers()  # 王炸测试
    test_repeated_cards()  # 普通炸测试
    test_cascaded_cards()  # 连对测试
    test_attached_cards()  # 带牌测试
    test_greater_cards()  # 大小测试


def test_empty_cardgroup():
    # 空卡组赋值测试
    try:
        CardGroup([])
    except ValueError as e:
        assert str(e) == "card length must be greater than 0, got 0"


def test_two_jokers():
    # 王炸测试
    cg = CardGroup([Card(Suit.OTHER, Rank.RED_JOKER)])
    assert cg.is_two_jokers() is False  # 一张王, False
    cg = CardGroup([Card(Suit.SPADE, Rank.QUEEN), Card(Suit.HEART, Rank.QUEEN)])
    assert cg.is_two_jokers() is False  # 两张普通牌, False
    cg = CardGroup([Card(Suit.OTHER, Rank.BLACK_JOKER), Card(Suit.OTHER, Rank.RED_JOKER)])
    assert cg.is_two_jokers() is True  # 小王+大王, True
    cg = CardGroup([Card(Suit.OTHER, Rank.RED_JOKER), Card(Suit.OTHER, Rank.BLACK_JOKER)])
    assert cg.is_two_jokers() is True  # 大王+小王, True


def test_repeated_cards():
    """重复牌测试"""
    cg = CardGroup([Card(Suit.HEART, Rank.QUEEN)])
    assert cg.is_repeated_cards() == (1, Rank.QUEEN)  # 1张普通牌
    cg = CardGroup([Card(Suit.SPADE, Rank.QUEEN), Card(Suit.HEART, Rank.QUEEN)])
    assert cg.is_repeated_cards() == (2, Rank.QUEEN)  # 两张普通牌
    cg = CardGroup([Card(Suit.SPADE, Rank.QUEEN), Card(Suit.HEART, Rank.QUEEN), Card(Suit.HEART, Rank.ACE)])
    assert cg.is_repeated_cards() == (False, False)  # 3张普通牌, 2张相同
    cg = CardGroup([Card(Suit.SPADE, Rank.QUEEN), Card(Suit.HEART, Rank.QUEEN), Card(Suit.CLUB, Rank.QUEEN)])
    assert cg.is_repeated_cards() == (3, Rank.QUEEN)  # 3张普通牌
    cg = CardGroup([
        Card(Suit.SPADE, Rank.QUEEN), Card(Suit.HEART, Rank.QUEEN), Card(Suit.DIAMOND, Rank.QUEEN),
        Card(Suit.CLUB, Rank.DEUCE)
    ])
    assert cg.is_repeated_cards() == (False, False)  # 4张普通牌，False
    cg = CardGroup([
        Card(Suit.SPADE, Rank.FIVE), Card(Suit.HEART, Rank.FIVE), Card(Suit.DIAMOND, Rank.FIVE),
        Card(Suit.CLUB, Rank.FIVE)
    ])
    assert cg.is_repeated_cards() == (4, Rank.FIVE)  # 4张相同牌，True


def test_cascaded_cards():
    """连对测试"""
    cg = CardGroup([
        Card(Suit.SPADE, Rank.FOUR), Card(Suit.HEART, Rank.FIVE),
        Card(Suit.DIAMOND, Rank.SIX)
    ])
    assert cg.is_cascaded_cards() == (False, False, False)  # 三张连着的不是
    cg = CardGroup([
        Card(Suit.OTHER, Rank.BLACK_JOKER), Card(Suit.HEART, Rank.FIVE),
        Card(Suit.DIAMOND, Rank.SIX), Card(Suit.HEART, Rank.SEVEN), Card(Suit.HEART, Rank.EIGHT),
    ])
    assert cg.is_cascaded_cards() == (False, False, False)  # 带王的不是
    cg = CardGroup([
        Card(Suit.HEART, Rank.THREE), Card(Suit.HEART, Rank.FOUR),
        Card(Suit.DIAMOND, Rank.FIVE), Card(Suit.HEART, Rank.SIX), Card(Suit.HEART, Rank.EIGHT),
    ])
    assert cg.is_cascaded_cards() == (False, False, False)  # 不连着的不是
    cg = CardGroup([
        Card(Suit.HEART, Rank.JACK), Card(Suit.HEART, Rank.QUEEN),
        Card(Suit.DIAMOND, Rank.KING), Card(Suit.HEART, Rank.ACE), Card(Suit.HEART, Rank.DEUCE),
    ])
    assert cg.is_cascaded_cards() == (False, False, False)  # 带2的不是
    cg = CardGroup([
        Card(Suit.HEART, Rank.TEN), Card(Suit.HEART, Rank.JACK), Card(Suit.HEART, Rank.QUEEN),
        Card(Suit.DIAMOND, Rank.KING), Card(Suit.HEART, Rank.ACE),
    ])
    assert cg.is_cascaded_cards() == (1, 5, Rank.TEN)  # 正常的一个连对

    cg = CardGroup([
        Card(Suit.HEART, Rank.TEN), Card(Suit.SPADE, Rank.TEN), Card(Suit.HEART, Rank.JACK),
        Card(Suit.DIAMOND, Rank.JACK), Card(Suit.DIAMOND, Rank.QUEEN), Card(Suit.HEART, Rank.QUEEN)
    ])
    assert cg.is_cascaded_cards() == (2, 3, Rank.TEN)  # 正常的一个双连对
    cg = CardGroup([
        Card(Suit.HEART, Rank.NINE), Card(Suit.SPADE, Rank.NINE), Card(Suit.HEART, Rank.JACK),
        Card(Suit.DIAMOND, Rank.JACK), Card(Suit.DIAMOND, Rank.QUEEN), Card(Suit.HEART, Rank.QUEEN)
    ])
    assert cg.is_cascaded_cards() == (False, False, False)  # 不是双连对
    cg = CardGroup([
        Card(Suit.HEART, Rank.NINE), Card(Suit.SPADE, Rank.NINE), Card(Suit.HEART, Rank.TEN),
        Card(Suit.DIAMOND, Rank.TEN)
    ])
    assert cg.is_cascaded_cards() == (False, False, False)  # 不是双连对
    cg = CardGroup([
        Card(Suit.HEART, Rank.TEN), Card(Suit.SPADE, Rank.TEN), Card(Suit.HEART, Rank.JACK),
        Card(Suit.DIAMOND, Rank.JACK), Card(Suit.DIAMOND, Rank.QUEEN)
    ])
    assert cg.is_cascaded_cards() == (False, False, False)  # 不是双连对
    cg = CardGroup([
        Card(Suit.HEART, Rank.TEN), Card(Suit.SPADE, Rank.TEN), Card(Suit.HEART, Rank.JACK),
        Card(Suit.DIAMOND, Rank.JACK), Card(Suit.SPADE, Rank.JACK), Card(Suit.CLUB, Rank.JACK)
    ])
    assert cg.is_cascaded_cards() == (False, False, False)  # 不是双连对

    cg = CardGroup([
        Card(Suit.DIAMOND, Rank.TEN), Card(Suit.SPADE, Rank.TEN), Card(Suit.HEART, Rank.TEN),
        Card(Suit.DIAMOND, Rank.JACK), Card(Suit.SPADE, Rank.JACK), Card(Suit.CLUB, Rank.JACK)
    ])
    assert cg.is_cascaded_cards() == (3, 2, Rank.TEN)  # 正常飞机
    cg = CardGroup([
        Card(Suit.DIAMOND, Rank.TEN), Card(Suit.SPADE, Rank.TEN), Card(Suit.HEART, Rank.TEN),
        Card(Suit.DIAMOND, Rank.JACK), Card(Suit.SPADE, Rank.JACK), Card(Suit.CLUB, Rank.JACK),
        Card(Suit.DIAMOND, Rank.JACK)
    ])
    assert cg.is_cascaded_cards() == (False, False, False)  # 不是飞机
    cg = CardGroup([
        Card(Suit.DIAMOND, Rank.NINE), Card(Suit.SPADE, Rank.NINE), Card(Suit.HEART, Rank.NINE),
        Card(Suit.DIAMOND, Rank.JACK), Card(Suit.SPADE, Rank.JACK), Card(Suit.CLUB, Rank.JACK),
    ])
    assert cg.is_cascaded_cards() == (False, False, False)  # 不是飞机
    cg = CardGroup([
        Card(Suit.DIAMOND, Rank.ACE), Card(Suit.SPADE, Rank.ACE), Card(Suit.HEART, Rank.ACE),
        Card(Suit.DIAMOND, Rank.DEUCE), Card(Suit.SPADE, Rank.DEUCE), Card(Suit.CLUB, Rank.DEUCE)
    ])
    assert cg.is_cascaded_cards() == (False, False, False)  # 不是飞机


def test_attached_cards():
    cg = CardGroup([
        Card(Suit.CLUB, Rank.THREE), Card(Suit.DIAMOND, Rank.THREE), Card(Suit.SPADE, Rank.THREE),
        Card(Suit.DIAMOND, Rank.SEVEN), Card(Suit.SPADE, Rank.SEVEN),
    ])
    assert cg.is_attached_cards() == (3, 2, Rank.THREE)  # 333 + 77

    cg = CardGroup([
        Card(Suit.CLUB, Rank.THREE), Card(Suit.DIAMOND, Rank.THREE), Card(Suit.SPADE, Rank.THREE),
        Card(Suit.DIAMOND, Rank.SIX), Card(Suit.SPADE, Rank.SEVEN),
    ])
    assert cg.is_attached_cards() == (False, False, False)

    cg = CardGroup([
        Card(Suit.CLUB, Rank.DEUCE), Card(Suit.DIAMOND, Rank.DEUCE), Card(Suit.SPADE, Rank.DEUCE),
        Card(Suit.DIAMOND, Rank.BLACK_JOKER)
    ])
    assert cg.is_attached_cards() == (3, 1, Rank.DEUCE)  # 222 + wang

    cg = CardGroup([
        Card(Suit.CLUB, Rank.DEUCE), Card(Suit.DIAMOND, Rank.DEUCE), Card(Suit.SPADE, Rank.DEUCE),
        Card(Suit.HEART, Rank.DEUCE), Card(Suit.CLUB, Rank.FIVE),
    ])
    assert cg.is_attached_cards() == (False, False, False)

    cg = CardGroup([
        Card(Suit.CLUB, Rank.DEUCE), Card(Suit.DIAMOND, Rank.DEUCE), Card(Suit.SPADE, Rank.DEUCE),
        Card(Suit.HEART, Rank.DEUCE), Card(Suit.CLUB, Rank.FIVE), Card(Suit.SPADE, Rank.FIVE),
    ])
    assert cg.is_attached_cards() == (False, False, False)

    cg = CardGroup([
        Card(Suit.CLUB, Rank.DEUCE), Card(Suit.DIAMOND, Rank.DEUCE), Card(Suit.SPADE, Rank.DEUCE),
        Card(Suit.HEART, Rank.DEUCE), Card(Suit.CLUB, Rank.JACK), Card(Suit.SPADE, Rank.FIVE),
    ])
    assert cg.is_attached_cards() == (4, 2, Rank.DEUCE)  # 2222+J5

    cg = CardGroup([
        Card(Suit.CLUB, Rank.QUEEN), Card(Suit.DIAMOND, Rank.QUEEN), Card(Suit.SPADE, Rank.QUEEN),
        Card(Suit.CLUB, Rank.JACK), Card(Suit.DIAMOND, Rank.JACK), Card(Suit.SPADE, Rank.JACK),
        Card(Suit.DIAMOND, Rank.SEVEN), Card(Suit.SPADE, Rank.DEUCE),
    ])
    assert cg.is_attached_cards() == (6, 2, Rank.QUEEN)  # JJJQQQ + 72

    cg = CardGroup([
        Card(Suit.CLUB, Rank.QUEEN), Card(Suit.DIAMOND, Rank.QUEEN), Card(Suit.SPADE, Rank.QUEEN),
        Card(Suit.CLUB, Rank.JACK), Card(Suit.DIAMOND, Rank.JACK), Card(Suit.SPADE, Rank.JACK),
        Card(Suit.DIAMOND, Rank.FOUR), Card(Suit.SPADE, Rank.FOUR),
        Card(Suit.DIAMOND, Rank.SIX), Card(Suit.SPADE, Rank.SIX),
    ])
    assert cg.is_attached_cards() == (6, 4, Rank.QUEEN)  # JJJQQQ + 4466

    cg = CardGroup([
        Card(Suit.CLUB, Rank.QUEEN), Card(Suit.DIAMOND, Rank.QUEEN), Card(Suit.SPADE, Rank.QUEEN),
        Card(Suit.CLUB, Rank.JACK), Card(Suit.DIAMOND, Rank.JACK), Card(Suit.SPADE, Rank.JACK),
        Card(Suit.CLUB, Rank.KING), Card(Suit.DIAMOND, Rank.KING), Card(Suit.SPADE, Rank.KING),
        Card(Suit.DIAMOND, Rank.FOUR), Card(Suit.SPADE, Rank.FOUR),
        Card(Suit.DIAMOND, Rank.SIX), Card(Suit.SPADE, Rank.SIX),
    ])
    assert cg.is_attached_cards() == (False, False, False)  # JJJQQQKKK + 4466

    cg = CardGroup([
        Card(Suit.CLUB, Rank.QUEEN), Card(Suit.DIAMOND, Rank.QUEEN), Card(Suit.SPADE, Rank.QUEEN),
        Card(Suit.CLUB, Rank.JACK), Card(Suit.DIAMOND, Rank.JACK), Card(Suit.SPADE, Rank.JACK),
        Card(Suit.CLUB, Rank.KING), Card(Suit.DIAMOND, Rank.KING), Card(Suit.SPADE, Rank.KING),
        Card(Suit.DIAMOND, Rank.FOUR), Card(Suit.SPADE, Rank.FOUR),
        Card(Suit.DIAMOND, Rank.SIX), Card(Suit.SPADE, Rank.SIX),
        Card(Suit.DIAMOND, Rank.ACE), Card(Suit.SPADE, Rank.ACE),
    ])
    assert cg.is_attached_cards() == (9, 6, Rank.KING)  # JJJQQQKKK + 4466AA


def test_greater_cards():
    # 牌组大小测试
    a = CardGroup([
        Card(Suit.OTHER, Rank.RED_JOKER), Card(Suit.OTHER, Rank.BLACK_JOKER)
    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.DEUCE), Card(Suit.HEART, Rank.DEUCE),
        Card(Suit.DIAMOND, Rank.DEUCE), Card(Suit.CLUB, Rank.DEUCE),
    ])
    assert a.is_greater(b) is True

    a = CardGroup([
        Card(Suit.OTHER, Rank.RED_JOKER)
    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.DEUCE), Card(Suit.HEART, Rank.DEUCE),
        Card(Suit.DIAMOND, Rank.DEUCE), Card(Suit.CLUB, Rank.DEUCE),
    ])
    assert a.is_greater(b) is False

    a = CardGroup([
        Card(Suit.OTHER, Rank.RED_JOKER), Card(Suit.OTHER, Rank.BLACK_JOKER)
    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.DEUCE), Card(Suit.HEART, Rank.DEUCE),
        Card(Suit.DIAMOND, Rank.DEUCE)
    ])
    assert a.is_greater(b) is True

    # AAA < 222
    a = CardGroup([
        Card(Suit.SPADE, Rank.ACE), Card(Suit.HEART, Rank.ACE),
        Card(Suit.DIAMOND, Rank.ACE)
    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.DEUCE), Card(Suit.HEART, Rank.DEUCE),
        Card(Suit.DIAMOND, Rank.DEUCE)
    ])
    assert a.is_greater(b) is False

    # 222 > AAA
    a = CardGroup([
        Card(Suit.SPADE, Rank.DEUCE), Card(Suit.HEART, Rank.DEUCE),
        Card(Suit.DIAMOND, Rank.DEUCE)

    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.ACE), Card(Suit.HEART, Rank.ACE),
        Card(Suit.DIAMOND, Rank.ACE)
    ])
    assert a.is_greater(b) is True

    # 大王 > 小王
    a = CardGroup([
        Card(Suit.OTHER, Rank.RED_JOKER)
    ])
    b = CardGroup([
        Card(Suit.OTHER, Rank.BLACK_JOKER)
    ])
    assert a.is_greater(b) is True

    # 小王 < 大王
    a = CardGroup([
        Card(Suit.OTHER, Rank.BLACK_JOKER)
    ])
    b = CardGroup([
        Card(Suit.OTHER, Rank.RED_JOKER)
    ])
    assert a.is_greater(b) is False

    # 2 > 5
    a = CardGroup([
        Card(Suit.DIAMOND, Rank.DEUCE)
    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.FIVE)
    ])
    assert a.is_greater(b) is True

    # 22 > 33
    a = CardGroup([
        Card(Suit.DIAMOND, Rank.DEUCE), Card(Suit.CLUB, Rank.DEUCE)
    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.THREE), Card(Suit.HEART, Rank.THREE)
    ])
    assert a.is_greater(b) is True

    # KKK > 999
    a = CardGroup([
        Card(Suit.DIAMOND, Rank.KING), Card(Suit.CLUB, Rank.KING), Card(Suit.SPADE, Rank.KING),
    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.NINE), Card(Suit.HEART, Rank.NINE), Card(Suit.DIAMOND, Rank.NINE)
    ])
    assert a.is_greater(b) is True

    # 3333 > 222
    a = CardGroup([
        Card(Suit.DIAMOND, Rank.THREE), Card(Suit.CLUB, Rank.THREE), Card(Suit.SPADE, Rank.THREE),
        Card(Suit.HEART, Rank.THREE)
    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.DEUCE), Card(Suit.HEART, Rank.DEUCE), Card(Suit.DIAMOND, Rank.DEUCE)
    ])
    assert a.is_greater(b) is True

    # 9998 > 6662
    a = CardGroup([
        Card(Suit.DIAMOND, Rank.NINE), Card(Suit.CLUB, Rank.NINE), Card(Suit.SPADE, Rank.NINE),
        Card(Suit.CLUB, Rank.EIGHT)
    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.SIX), Card(Suit.HEART, Rank.SIX), Card(Suit.DIAMOND, Rank.SIX),
        Card(Suit.HEART, Rank.DEUCE)
    ])
    assert a.is_greater(b) is True

    # 9998 334455
    a = CardGroup([
        Card(Suit.DIAMOND, Rank.NINE), Card(Suit.CLUB, Rank.NINE), Card(Suit.SPADE, Rank.NINE),
        Card(Suit.CLUB, Rank.EIGHT)
    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.THREE), Card(Suit.HEART, Rank.THREE), Card(Suit.DIAMOND, Rank.FOUR),
        Card(Suit.HEART, Rank.FOUR), Card(Suit.DIAMOND, Rank.FIVE), Card(Suit.HEART, Rank.FIVE)
    ])
    assert a.is_greater(b) is False

    # 10JQKA > 34567
    a = CardGroup([
        Card(Suit.SPADE, Rank.TEN), Card(Suit.HEART, Rank.JACK), Card(Suit.DIAMOND, Rank.QUEEN),
        Card(Suit.HEART, Rank.KING), Card(Suit.DIAMOND, Rank.ACE)
    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.THREE), Card(Suit.HEART, Rank.FOUR), Card(Suit.DIAMOND, Rank.FIVE),
        Card(Suit.HEART, Rank.SEVEN), Card(Suit.DIAMOND, Rank.SIX)
    ])
    assert a.is_greater(b) is True

    # 10JQKA 345678
    a = CardGroup([
        Card(Suit.SPADE, Rank.TEN), Card(Suit.HEART, Rank.JACK), Card(Suit.DIAMOND, Rank.QUEEN),
        Card(Suit.HEART, Rank.KING), Card(Suit.DIAMOND, Rank.ACE)
    ])
    b = CardGroup([
        Card(Suit.SPADE, Rank.THREE), Card(Suit.HEART, Rank.FOUR), Card(Suit.DIAMOND, Rank.FIVE),
        Card(Suit.HEART, Rank.SEVEN), Card(Suit.DIAMOND, Rank.SIX), Card(Suit.DIAMOND, Rank.EIGHT)
    ])
    assert a.is_greater(b) is False


if __name__ == '__main__':
    test()
