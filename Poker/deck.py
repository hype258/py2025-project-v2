import random
from card import Card

import random
from card import Card

class Deck:

    def __init__(self):
        # Tworzy niepotasowaną talię 52 kart
        self.cards = [Card(rank, suit) for suit in ['s', 'h', 'd', 'c']
                                         for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]

    def __str__(self):
        # Reprezentacja talii jako string
        return ', '.join(map(str, self.cards))

    def shuffle(self):
        # Tasuje talię
        random.shuffle(self.cards)

    def deal(self, n):
        return [self.cards.pop() for _ in range(n)]
