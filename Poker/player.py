from Poker.game_logic import hand_rank

class Player:

    def __init__(self, money, name="", is_bot=False):
        self.stack = money
        self.name = name
        self.hand = []
        self.is_bot = is_bot
        self.folded = False

    def take_card(self, card):
        # Dodaje jedną kartę do ręki
        self.hand.append(card)

    def get_player_hand(self):
        # Zwraca rękę jako krotkę
        return tuple(self.hand)

    def change_card(self, card, idx):
        # Wymienia kartę na pozycji idx na nową, zwraca starą
        old_card = self.hand[idx]
        self.hand[idx] = card
        return old_card

    def get_stack_amount(self):
        return self.stac

    def cards_to_str(self):
        # Zwraca rękę jako jeden string np. "A♠ 10♦ 2♣ 7♥ J♣"
        return ' '.join(map(str, self.hand))


