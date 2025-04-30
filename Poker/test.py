from Poker.game_logic import hand_rank
from deck import Deck
from player import Player

deck = Deck()
deck.shuffle()

player1 = Player("Mariusz")
player2 = Player("Bogdan")

player1.receive_cards(deck.deal(5))
player2.receive_cards(deck.deal(5))

print(player1.name, ":", player1.show_hand())
print(player2.name, ":", player2.show_hand())
print(player1.hand_rank())
print(player2.hand_rank())
player1.exchange_cards([3, 4], deck)
print("Po wymianie:")
print(player1.show_hand())
print(player1.hand_rank())