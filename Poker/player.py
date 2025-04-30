from Poker.game_logic import hand_rank


class Player:
    def __init__(self, name, stack=100):
        self.name = name
        self._stack = stack
        self.hand = []

    @property
    def stack(self):
        return self._stack

    @stack.setter
    def stack(self, value):
        if value < 0:
            raise ValueError("Stack can't be negative")
        self._stack = value

    def receive_cards(self, cards):
        self.hand = cards

    def show_hand(self):
        return ' '.join(map(str, self.hand))

    def bet(self, amount):
        if amount > self.stack:
            raise ValueError(f"{self.name} does not have enough chips to bet {amount}")
        self.stack -= amount
        return amount

    def exchange_cards(self, indices, deck):
        for i in sorted(indices, reverse=True):
            self.hand.pop(i)
        new_cards = deck.deal(len(indices))
        self.hand.extend(new_cards)

    def hand_rank(self):
        return hand_rank(self.hand)

    def __str__(self):
        return f"{self.name}: {self.show_hand()} | Chips: {self.stack}"
