import random
from player import Player

class BotPlayer(Player):
    def __init__(self, name="Bot", money=500):
        super().__init__(money, name)
        self.is_bot = True

    def choose_discard_indices(self):
        """Bot losowo decyduje, które karty wymienić (np. 0–3 karty)."""
        how_many = random.randint(0, 3)
        return sorted(random.sample(range(5), how_many))

    def decide_action(self, current_bet):
        """Bot podejmuje decyzję: call, raise lub fold."""
        if self.stack <= current_bet:
            return "call"
        action = random.choice(["call", "raise", "fold"])
        if action == "raise":
            raise_amount = min(50, self.stack - current_bet)
            return f"raise {raise_amount}"
        return action
