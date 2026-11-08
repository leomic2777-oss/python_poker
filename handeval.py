from itertools import combinations
from collections import Counter

def card_value(card):
    """Convert card keys such as CA, D10 and S5 into rank and suit."""
    suit = card[0]
    rank_text = card[1:].upper()

    ranks = {
        "2": 2, "3": 3, "4": 4, "5": 5,
        "6": 6, "7": 7, "8": 8, "9": 9,
        "10": 10, "J": 11, "Q": 12,
        "K": 13, "A": 14
    }

    if suit not in "CDHS" or rank_text not in ranks:
        raise ValueError(f"Invalid card key: {card}")

    return ranks[rank_text], suit


def evaluate_five(cards):
    """Return a comparable score for exactly five poker cards."""
    parsed = [card_value(card) for card in cards]
    values = sorted((rank for rank, suit in parsed), reverse=True)
    suits = [suit for rank, suit in parsed]

    counts = Counter(values)
    groups = sorted(
        counts.items(),
        key=lambda item: (item[1], item[0]),
        reverse=True
    )

    flush = len(set(suits)) == 1

    unique_values = sorted(set(values), reverse=True)
    straight_high = 0

    if len(unique_values) == 5:
        if unique_values[0] - unique_values[4] == 4:
            straight_high = unique_values[0]
        elif unique_values == [14, 5, 4, 3, 2]:
            straight_high = 5

    # 8: Straight flush
    if flush and straight_high:
        return (8, straight_high)

    # 7: Four of a kind
    if groups[0][1] == 4:
        four_rank = groups[0][0]
        kicker = max(v for v in values if v != four_rank)
        return (7, four_rank, kicker)

    # 6: Full house
    if sorted(counts.values()) == [2, 3]:
        trips = groups[0][0]
        pair = groups[1][0]
        return (6, trips, pair)

    # 5: Flush
    if flush:
        return (5, *values)

    # 4: Straight
    if straight_high:
        return (4, straight_high)

    # 3: Three of a kind
    if groups[0][1] == 3:
        trips = groups[0][0]
        kickers = sorted(
            (v for v in values if v != trips), reverse=True
        )
        return (3, trips, *kickers)

    # 2: Two pair
    pairs = sorted(
        (rank for rank, count in counts.items() if count == 2),
        reverse=True
    )
    if len(pairs) == 2:
        kicker = max(v for v in values if v not in pairs)
        return (2, pairs[0], pairs[1], kicker)

    # 1: One pair
    if len(pairs) == 1:
        pair = pairs[0]
        kickers = sorted(
            (v for v in values if v != pair), reverse=True
        )
        return (1, pair, *kickers)

    # 0: High card
    return (0, *values)


def evalhand(cards):
    """Find the strongest five-card hand from five to seven cards."""
    if len(cards) < 5:
        raise ValueError("At least five cards are required.")

    return max(
        evaluate_five(combo)
        for combo in combinations(cards, 5)
    )

