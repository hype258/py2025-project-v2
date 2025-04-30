class Card:
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    suit_symbols = {
        'Clubs': '\u2663',
        'Diamonds': '\u2666',
        'Hearts': '\u2665',
        'Spades': '\u2660'
    }

    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit_symbols[self.suit]}"

    def __repr__(self):
        return self.__str__()

