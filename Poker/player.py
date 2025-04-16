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
