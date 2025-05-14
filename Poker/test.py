from Poker.game_logic import hand_rank
from deck import Deck
from player import Player

deck = Deck()
deck.shuffle()

players = [Player(100, name="Alice"), Player(100, name="Bob")]

engine = GameEngine(players, deck)
engine.play_round()
