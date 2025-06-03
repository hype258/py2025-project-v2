class Card:
    # słownik symboli unicode
    unicode_dict = {'s': '\u2660', 'h': '\u2665', 'd': '\u2666', 'c': '\u2663'}

    def __init__(self, rank, suit):
        # rank to np. 'A', '10', 'J', '3'
        # suit to pojedynczy znak: 's', 'h', 'd', 'c'
        self.rank = rank
        self.suit = suit

    def get_value(self):
        # zwraca krotkę, np. ('A', 's')
        return (self.rank, self.suit)

    def __str__(self):
        # wypisuje np. A♠ lub 10♦
        return f"{self.rank}{Card.unicode_dict[self.suit]}"

    def __repr__(self):
        return self.__str__()

