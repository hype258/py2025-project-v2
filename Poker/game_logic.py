from collections import Counter

RANK_ORDER = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
              '10':10, 'J':11, 'Q':12, 'K':13, 'A':14}

def hand_rank(cards):
    ranks = [card.rank for card in cards]
    suits = [card.suit for card in cards]
    values = sorted([RANK_ORDER[rank] for rank in ranks], reverse=True)
    rank_counts = Counter(ranks)
    count_values = sorted(rank_counts.values(), reverse=True)

    is_flush = len(set(suits)) == 1
    is_straight = len(set(values)) == 5 and values[0] - values[-1] == 4

    # Royal Flush
    if is_flush and values == [14, 13, 12, 11, 10]:
        return ('Royal Flush', 10)

    # Straight Flush
    if is_flush and is_straight:
        return ('Straight Flush', 9)

    # Four of a Kind
    if count_values == [4, 1]:
        return ('Four of a Kind', 8)

    # Full House
    if count_values == [3, 2]:
        return ('Full House', 7)

    # Flush
    if is_flush:
        return ('Flush', 6)

    # Straight
    if is_straight:
        return ('Straight', 5)

    # Three of a Kind
    if count_values == [3, 1, 1]:
        return ('Three of a Kind', 4)

    # Two Pair
    if count_values == [2, 2, 1]:
        return ('Two Pair', 3)

    # One Pair
    if count_values == [2, 1, 1, 1]:
        return ('One Pair', 2)

    # High Card
    return ('High Card', 1)
